import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from './stores/UserStore.ts';
import plans from './views/Plan.vue';
import login from './views/Login.vue';
import register from './views/Register.vue';
import homepage from './views/HomePage.vue';
import projects from './views/Projects.vue';
import editprofile from './views/EditProfile.vue';
import profile from './views/Profile.vue';
import ProjectPage from './views/ProjectPage.vue';
import ImageEditor from './views/ImageEditor.vue';

const routes = [
    { path: '/', component: homepage },
    { path: '/plans', component: plans },
    { path: '/login', component: login },
    { path: '/register', component: register },
    { path: '/edit-profile', component: editprofile },
    { path: '/profile', component: profile },
    { path: '/projects', component: projects },
    { path: '/projects?:projectId', name: 'ProjectPage', component: ProjectPage },
    { path: '/image-editor', component: ImageEditor },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    if (!userStore.isLoggedIn && to.path !== '/login' && to.path !== '/register') {
        next();
    } else {
        next();
    }
});

export default router;
