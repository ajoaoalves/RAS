// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import plans from './views/Plan.vue';

const routes = [
  { path: '/', component: plans, name: 'Home' }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
