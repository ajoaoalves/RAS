import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {
            id: '',
            name: '',
            email: '',
            type: ''
        },
        isLoggedIn: false,
    }),
    actions: {
        setUser(user) {
            console.log('setUser', user);
            this.user = user;
            this.isLoggedIn = true;
            localStorage.setItem('user', JSON.stringify(user));  // Salva o usuário no localStorage
        },
        clearUser() {
            this.user = { id: '', name: '', email: '', type: '' };
            this.isLoggedIn = false;
            localStorage.removeItem('user');  // Remove o usuário do localStorage
        },
    },
    getters: {
        userName: (state) => state.user.name,
        isAuthenticated: (state) => state.isLoggedIn,
    },
});