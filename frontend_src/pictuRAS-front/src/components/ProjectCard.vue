<template>
    <div class="project-card" @click="navigateToProject">
        <div class="project-content">
            <h2>{{ project.name }}</h2>
        </div>
        <button
            class="delete-button"
            @click.stop="showConfirmationModal"
        >
            Delete
        </button>

        <ConfirmationModal
            :visible="isModalVisible"
            :projectName="project.name"
            @confirm="deleteProject"
            @cancel="closeModal"
        />
    </div>
</template>

<script>
import ConfirmationModal from "./confirmation.vue";
import { useProjectStore } from "../stores/ProjectStore";

export default {
    components: { ConfirmationModal },
    props: {
        project: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            isModalVisible: false,
        };
    },
    methods: {
        showConfirmationModal() {
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        deleteProject() {
            this.$emit("delete", this.project._id);
            this.isModalVisible = false;
        },
        navigateToProject() {
            const projectStore = useProjectStore();
            projectStore.setProject(this.project);
            this.$router.push({ name: "ProjectPage", params: { projectId: this.project._id } });
        },
    },
};
</script>


<style scoped>
  .project-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
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
  </style>
  