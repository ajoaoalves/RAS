// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import plans from './views/Plan.vue';

const routes = [
  { path: '/plans', component: plans },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
