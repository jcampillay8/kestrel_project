import threading
import logging

class EmailThread(threading.Thread):
    """
    Clase para enviar correos electrónicos en un hilo separado.
    """

    def __init__(self, email):
        """
        Inicializa la clase con el correo electrónico a enviar.
        """
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """
        Envía el correo electrónico y captura posibles excepciones.
        """
        try:
            self.email.send(fail_silently=False)
        except Exception as e:
            logging.error(f"Error al enviar el correo: {e}")
