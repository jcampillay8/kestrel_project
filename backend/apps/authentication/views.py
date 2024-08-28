import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext as _
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Hilo para el envío de correos electrónicos
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

# Vista para validar correos electrónicos
class EmailValidationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not validate_email(email):
            return Response({'email_error': _('Email is invalid')}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'email_error': _('Sorry, email is already in use. Choose another one.')}, status=status.HTTP_409_CONFLICT)
        return Response({'email_valid': True}, status=status.HTTP_200_OK)

# Vista para validar nombres de usuario
class UsernameValidationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        if not username.isalnum():
            return Response({'error': _('Username can only contain letters and numbers')}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': _('Username is taken, please choose a new one')}, status=status.HTTP_409_CONFLICT)
        return Response({'is_available': True}, status=status.HTTP_200_OK)

class CredentialsValidationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        if not email:
            return Response({'error': _('Please enter an email')}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar si el email tiene un formato válido
        if not validate_email(email):
            return Response({'error': _('Please enter a valid email')}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si el correo ya existe en la base de datos
        if User.objects.filter(email=email).exists():
            return Response({'error': _('Email is taken, please choose a new one')}, status=status.HTTP_409_CONFLICT)
        
        return Response({'valid': True}, status=status.HTTP_200_OK)

# Vista para el registro de usuarios
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if first_name and last_name and username and email and password:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password) < 6:
                        return Response({'error': _('Password too short')}, status=status.HTTP_400_BAD_REQUEST)

                    # Crear usuario
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user.set_password(password)
                    user.is_active = False
                    user.save()

                    # Envío de correo de activación
                    current_site = get_current_site(request)
                    email_body = {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }
                    link = reverse('activate', kwargs={
                        'uidb64': email_body['uid'],
                        'token': email_body['token']
                    })
                    activate_url = 'http://' + current_site.domain + link
                    email_subject = _('Activate your account')
                    email_message = EmailMessage(
                        email_subject,
                        _('Hi ')+user.username + _(', Please use the link below to activate your account \n') + activate_url,
                        'noreply@example.com',
                        [email],
                    )
                    EmailThread(email_message).start()
                    return Response({'message': _('We have sent you an email with a validation link. Please check your email.')}, status=status.HTTP_201_CREATED)

        return Response({'error': _('Please fill all fields')}, status=status.HTTP_400_BAD_REQUEST)

# Vista para la activación de cuenta
class VerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not account_activation_token.check_token(user, token):
                return Response({'error': _('Invalid activation link')}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()
            return Response({'message': _('Account activated successfully')}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': _('Invalid activation link')}, status=status.HTTP_400_BAD_REQUEST)

# Vista para el login de usuarios
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')

        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user and user.is_active:
                login(request, user)
                return Response({'message': _('Login successful')}, status=status.HTTP_200_OK)
            return Response({'error': _('Invalid credentials or inactive account')}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'error': _('Please fill all fields')}, status=status.HTTP_400_BAD_REQUEST)

# Vista para el logout de usuarios
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': _('You have been logged out')}, status=status.HTTP_200_OK)

# Vista para solicitar restablecimiento de contraseña
class RequestPasswordResetEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email and validate_email(email):
            current_site = get_current_site(request)
            user = User.objects.filter(email=email).first()
            if user:
                email_contents = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': PasswordResetTokenGenerator().make_token(user),
                }
                link = reverse('reset-user-password', kwargs={
                    'uidb64': email_contents['uid'],
                    'token': email_contents['token']
                })
                reset_url = 'http://' + current_site.domain + link
                email_message = EmailMessage(
                    _('Password Reset Instructions'),
                    _('Hi there, Please use the link below to reset your password \n') + reset_url,
                    'noreply@example.com',
                    [email],
                )
                EmailThread(email_message).start()
                return Response({'message': _('We have sent you an email to reset your password')}, status=status.HTTP_200_OK)

        return Response({'error': _('Invalid email')}, status=status.HTTP_400_BAD_REQUEST)

# Vista para completar el restablecimiento de contraseña
class CompletePasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if password != password2:
            return Response({'error': _('Passwords do not match')}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({'error': _('Password too short')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': _('Invalid reset link')}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            return Response({'message': _('Password reset successfully')}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': _('Invalid reset link')}, status=status.HTTP_400_BAD_REQUEST)
