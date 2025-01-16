// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import plans from './views/Plan.vue';
import login from './views/Login.vue';

const routes = [
  { path: '/plans', component: plans },
  { path: '/login', component: login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
