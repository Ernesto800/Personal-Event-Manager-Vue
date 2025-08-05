import { createRouter, createWebHistory } from 'vue-router';
import HomeViewComponent from '../views/HomeViewComponent.vue';
import RegisterForm from '../views/RegisterFormComponent.vue';
import LoginForm from '../views/LoginForm.vue';
import EventsDashboardComponent from '../views/EventsDashboardComponent.vue';
import { isAuthenticated } from '../stores/auth';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeViewComponent,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterForm,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
  },
  {
    path: '/events',
    name: 'Events',
    component: EventsDashboardComponent,
    meta: { requiresAuth: true },
  },
 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {

  if (to.meta.requiresAuth && !isAuthenticated.value) {

    next('/login');
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated.value) {
    next('/events');
  } else {
    next();
  }
});




export default router;