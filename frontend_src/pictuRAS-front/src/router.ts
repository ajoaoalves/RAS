// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import plans from './views/Plan.vue';
import login from './views/Login.vue';
import register from './views/Register.vue';
import homepage from './views/HomePage.vue';
import projects from './views/Projects.vue';
import profile from './views/Profile.vue';
import ProjectPage from './views/ProjectPage.vue';

const routes = [
  { path: '/', component: homepage },
  { path: '/plans', component: plans },
  { path: '/login', component: login },
  { path: '/register', component: register },
  { path: '/profile', component: profile },
  { path: '/projects', component: projects },
  { path: '/projects:id', name: 'ProjectPage', component: ProjectPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
