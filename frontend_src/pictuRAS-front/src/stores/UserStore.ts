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
        setUser(user: { id: string; name: string; email: string ; type: string }) {
            this.user = user;
            this.isLoggedIn = true;
        },
        clearUser() {
            this.user = { id: '', name: '', email: '' , type: ''};
            this.isLoggedIn = false;
        },
    },
    getters: {
        userName: (state) => state.user.name,
        isAuthenticated: (state) => state.isLoggedIn,
    },
});