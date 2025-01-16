// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import plans from './views/Plan.vue';
import login from './views/Login.vue';
import register from './views/Register.vue';

const routes = [
  { path: '/plans', component: plans },
  { path: '/login', component: login },
  { path: '/register', component: register },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
