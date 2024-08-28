import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import ResetPassword from '../views/ResetPassword.vue';
import SetNewPassword from '../views/SetNewPassword.vue';
import Welcome from '../views/Welcome.vue';

const routes = [
  { path: '/', name: 'Welcome', component: Welcome },
  { path: '/home', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/reset-password', name: 'ResetPassword', component: ResetPassword },
  { path: '/set-new-password/:uidb64/:token', name: 'SetNewPassword', component: SetNewPassword },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
