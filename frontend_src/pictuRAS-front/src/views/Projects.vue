<template>
    <div class="projects-view">
      <Navbar />
      <header class="projects-header">
        <h1>Your Projects</h1>
      </header>
      <section class="projects-list">
        <ProjectCard
          v-for="project in projects"
          :key="project._id"
          :project="project"
          @delete="deleteProject(project._id)"
        />
        <div v-if="projects.length === 0" class="no-projects">
          <p>No projects found. Start by creating a new one!</p>
        </div>
      </section>
      <!-- Button to trigger modal -->
      <button class="add-project-button" @click="showCreateProjectModal">
        + New Project
      </button>
      <!-- Modal for creating new projects -->
      <div v-if="isModalVisible" class="modal-overlay">
        <div class="modal">
          <h2>Create New Project</h2>
          <form @submit.prevent="createProject">
            <label for="projectName">Project Name:</label>
            <input
              type="text"
              id="projectName"
              v-model="newProjectName"
              placeholder="Enter project name"
              required
            />
            <div class="modal-actions">
              <button type="submit" class="submit-button">Create</button>
              <button type="button" class="cancel-button" @click="closeModal">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>

  <script>
  import Navbar from "../components/Navbar.vue";
  import ProjectCard from "../components/ProjectCard.vue";
  import axios from 'axios';
  import { useUserStore } from '../stores/UserStore';
  import { useProjectStore } from '../stores/ProjectStore';

  export default {
    name: "ProjectsView",
    components: {
      Navbar,
      ProjectCard,
    },
    data() {
      return {
        projects: [],
        isModalVisible: false,
        newProjectName: "",
      };
    },
    mounted() {
      const userStore = useUserStore();
      console.log('User:', userStore.user);
      // Se o usuário não estiver autenticado, redireciona para a página de login
      if (!userStore.isLoggedIn) {
        this.$router.push('/login');
        return;
      }

      // Se o usuário estiver autenticado, faz a busca dos projetos
      this.fetchProjects();
    },
    methods: {
      async fetchProjects() {
        const userStore = useUserStore();
        try {
          const response = await axios.get(`users/${userStore.user.id}/projects`);
          //const response = await axios.get('/projects');
          this.projects = response.data;
        } catch (error) {
          console.error('Error fetching projects:', error);
          alert('Failed to fetch projects');
        }
      },
      showCreateProjectModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
        this.newProjectName = "";
      },
      async createProject() {
        const userStore = useUserStore();
        if (this.newProjectName) {
          const newProject = { name: this.newProjectName , user_id: userStore.user.id, tools: [], images: []};
          try {
            const response = await axios.post(`/users/${userStore.user.id}/projects`, newProject);
            this.projects.push(response.data);
            this.closeModal();
          } catch (error) {
            console.error('Error creating project:', error);
            alert('Failed to create project');
          }
        }
      },
      deleteProject(projectId) {
        const userStore = useUserStore();
        try {
          axios.delete(`/users/${userStore.user.id}/projects/${projectId}`);
          console.log('Deleted project:', projectId);
          this.projects = this.projects.filter((project) => project._id !== projectId);
          console.log('Projects:', this.projects);
        } catch (error) {
          console.error('Error deleting project:', error);
          alert('Failed to delete project');
        }
      },
    },
  };
  </script>


<style scoped>
.projects-view {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #f4f4f9;
  min-height: 100vh;
  margin-top: 30px;
}

.projects-header {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  margin-bottom: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center; /* Ensure the text is centered */
}

.projects-header h1 {
  font-size: 2rem;
  margin: 0; /* Remove default margin for better centering */
}

.projects-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto; /* Centers the grid */
  padding: 10px;
  box-sizing: border-box;
}

.add-project-button {
  margin: 20px auto;
  display: block;
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.add-project-button:hover {
  background-color: #218838;
  transform: scale(1.05);
}

.project-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  transition: transform 0.2s ease;
}

.project-card:hover {
  transform: translateY(-5px);
}

.project-content h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.delete-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.no-projects {
  text-align: center;
  color: #555;
  font-size: 1.2rem;
}

/* Modal overlay - centers the modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  z-index: 1000;
}

/* Center the modal */
.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  width: 400px;
  max-width: 90%;
  text-align: center; /* Center the form content */
  color: #333;
}

.modal h2 {
  margin: 0 0 20px;
}

.modal form {
  display: flex;
  flex-direction: column; /* Stack form elements vertically */
  align-items: center; /* Center the form content */
}

.modal form label {
  display: block;
  margin: 10px 0 5px;
  width: 100%; /* Take full width for alignment */
}

.modal form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: center; /* Center the buttons */
}

.submit-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.submit-button:hover {
  background-color: #0056b3;
}

.cancel-button:hover {
  background-color: #5a6268;
}
</style>
