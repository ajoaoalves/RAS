import { defineStore } from 'pinia';

export const useProjectStore = defineStore('project', {
    state: () => ({
        project: {
            id: '',
            name: ''
        }
    }),
    actions: {
        setProject(project: { id: string; name: string }) {
            this.project = project;
        },
        clearProject() {
            this.project = { id: '', name: '' };
        },
    },
    getters: {
        projectID: (state) => state.project.id,
    },
});