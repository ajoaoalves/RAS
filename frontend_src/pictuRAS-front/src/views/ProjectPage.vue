<template>
    <div class="dashboard">
      <Navbar />
  
      <!-- Header Section -->
      <header class="dashboard-header">
        <h1>Project Dashboard: {{ projectName }}</h1>
        <button class="save-button" @click="saveProject">Save Project</button>
      </header>
  
      <!-- Main Content -->
      <div class="dashboard-main">
        <!-- Upload Images Section -->
        <section class="upload-section">
          <h2>Upload Images</h2>
          <input type="file" multiple @change="uploadImages" accept="image/*" />
          <p v-if="uploadError" class="error">{{ uploadError }}</p>
          <div class="uploaded-images">
            <h3>Uploaded Images:</h3>
            <ul>
              <li v-for="(image, index) in projectImages" :key="index">
                <img
                  :src="image.url"
                  :alt="image.name"
                  class="thumbnail"
                  @click="selectImage(index)"
                />
                {{ image.name }}
                <button class="delete-button" @click="deleteImage(index)">Delete</button>
              </li>
            </ul>
          </div>
        </section>
  
        <!-- Tools Section -->
        <section class="tools-section">
          <h2>Tools</h2>
          <div class="tools-grid">
            <ToolComponent
              v-for="tool in availableTools"
              :key="tool.id"
              :tool="tool"
              @applyTool="applyTool"
            />
          </div>
        </section>
        <section class="toolchain-section">
          <h2>Toolchain</h2>
          <ul class="toolchain-list">
            <li
              v-for="(tool, index) in selectedTools"
              :key="index"
              class="toolchain-item"
            >
              <span>{{ tool.procedure }} (Instance {{ index + 1 }})</span>
              <button @click="editTool(index)" class="edit-button">Edit</button>
              <button @click="removeTool(index)" class="remove-button">Remove</button>
              <button
                @click="moveTool(index, -1)"
                :disabled="index === 0"
                class="move-button"
              >
                ↑
              </button>
              <button
                @click="moveTool(index, 1)"
                :disabled="index === selectedTools.length - 1"
                class="move-button"
              >
                ↓
              </button>
            </li>
          </ul>
          <button class="process-button" @click="processImages">Process Images</button>
        </section>
        <!-- Preview Section -->
        <section class="preview-section">
          <h2>Preview</h2>
          <div v-if="selectedImage !== null" class="preview-container">
            <h3>{{ projectImages[selectedImage].name }}</h3>
            <div
              v-for="(step, stepIndex) in selectedTools"
              :key="stepIndex"
              class="preview-thumbnail"
            >
              <img
                :src="projectImages[selectedImage].url"
                :alt="`Preview Step ${stepIndex + 1}`"
                class="thumbnail"
                @click="openImage(projectImages[selectedImage].url)"
              />
              <p>Step {{ stepIndex + 1 }}: {{ step.name }}</p>
            </div>
          </div>
          <p v-else>No image selected. Click on an image to view its preview.</p>
        </section>
  
        <!-- Toolchain Section -->
        
  
        <!-- Edit Tool Modal -->
        <div
    v-if="editingTool !== null && selectedTools[editingTool] && selectedTools[editingTool].parameters && selectedTools[editingTool].parameters.length > 0"
    class="modal"
    @click="closeEditModal"
  >
    <div class="modal-content" @click.stop>
      <h3>Edit Tool: {{ selectedTools[editingTool].procedure }}</h3>
      <div v-for="(param, index) in selectedTools[editingTool].parameters" :key="index">
        <label :for="param.name">{{ param.name }}</label>
        <input
          v-if="typeof param.value === 'number' || typeof param.value === 'string'"
          :type="typeof param.value === 'number' ? 'number' : 'text'"
          :id="param.name"
          v-model="selectedTools[editingTool].parameters[index].value"
        />
      </div>
      <button class="save-button" @click="saveToolEdits">Save</button>
    </div>
</div>  
        <!-- Modal Section for Image Zoom -->
        <div v-if="zoomedImage" class="modal" @click="zoomedImage = null">
          <img :src="zoomedImage" alt="Zoomed Image" class="zoomed-image" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from "../components/Navbar.vue";
  import ToolComponent from "../components/ToolComponent.vue";
  import axios from "axios";
  import { useUserStore } from "../stores/UserStore";
  import { useProjectStore } from "../stores/ProjectStore";
  
  export default {
    name: "ProjectDashboard",
    components: { Navbar, ToolComponent },
    mounted() {
      this.fetchProjectData();
    },
    props: {
      projectId: {
        type: String,
        required: true,
      },
      projectName: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        projectImages: [],
        selectedTools: [],
        availableTools: [
          {
            id: 1,
            name: "Rotate",
            parameters: [{ name: "angle", label: "Angle (degrees)", type: "number", value: 0 }],
          },
          {
            id: 2,
            name: "Crop",
            parameters: [
              { name: "width", label: "Width (px)", type: "number", value: 100 },
              { name: "height", label: "Height (px)", type: "number", value: 100 },
            ],
          },
          {
            id: 3,
            name: "Resize",
            parameters: [{ name: "scale", label: "Scale (factor)", type: "number", value: 1 }],
          },
          {
            id: 4,
            name: "Adjust Brightness",
            parameters: [{ name: "brightness", label: "Brightness (%)", type: "number", value: 100 }],
          },
        ],
        uploadError: "",
        zoomedImage: null,
        selectedImage: null,
        editingTool: null,
      };
    },
    methods: {
      async fetchProjectData() {
      const userStore = useUserStore();
      const projectStore = useProjectStore();
      try {
        const response = await axios.get(`/users/${userStore.user.id}/projects/${projectStore.project._id}`);
        const { images, tools } = response.data;
        this.projectImages = images.map((image) => ({
          url: image.uri,
          name: image._id,
        }));
        this.selectedTools = tools;
        console.log("Project data loaded successfully:", response.data);
      } catch (error) {
        console.error("Error loading project data:", error.message);
        alert("Failed to load project data. Please refresh the page.");
      }
    },
      uploadImages(event) {
        const files = Array.from(event.target.files);
        files.forEach((file) => {
          if (file.size <= 5 * 1024 * 1024) {
            const reader = new FileReader();
            reader.onload = () => {
              this.projectImages.push({ url: reader.result, name: file.name });
            };
            reader.readAsDataURL(file);
          } else {
            this.uploadError = "Some files exceed the 5MB limit and were skipped.";
          }
        });
      },
      deleteImage(index) {
        if (this.selectedImage === index) {
          this.selectedImage = null;
        }
        this.projectImages.splice(index, 1);
      },
      applyTool(tool) {
        const newToolInstance = { ...tool, parameters: JSON.parse(JSON.stringify(tool.parameters)), id: Date.now() };
        this.selectedTools.push(newToolInstance);
      },
      removeTool(index) {
        this.selectedTools.splice(index, 1);
      },
      editTool(index) {
  const tool = this.selectedTools[index];
  if (tool && tool.parameters && Object.keys(tool.parameters).length > 0) {
    this.editingTool = index;
  } else {
    console.warn("No parameters found for the selected tool:", tool);
    this.editingTool = null;
  }
},

      saveToolEdits() {
        this.editingTool = null;
      },
      closeEditModal() {
        this.editingTool = null;
      },
      moveTool(index, direction) {
        const newIndex = index + direction;
        const temp = this.selectedTools[index];
        this.selectedTools[index] = this.selectedTools[newIndex];
        this.selectedTools[newIndex] = temp;
      },
      processImages() {
        console.log("Processing images with toolchain:", this.selectedTools);
      },
      saveProject() {
        console.log("Saving project...");
      },
      selectImage(index) {
        this.selectedImage = index;
      },
      openImage(url) {
        this.zoomedImage = url;
      },
    },
  };
  </script>
  
  <style scoped>
  .dashboard {
    font-family: Arial, sans-serif;
    color: #333;
    padding: 20px;
    background: #f9f9f9;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .dashboard-main {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .upload-section,
  .tools-section,
  .preview-section,
  .toolchain-section {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 15px;
  }
  
  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
  
  .preview-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .preview-thumbnail {
    text-align: center;
  }
  
  .toolchain-list {
    list-style: none;
    padding: 0;
  }
  
  .toolchain-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .thumbnail {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .zoomed-image {
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
    max-width: 90%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  button {
    padding: 5px 10px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
  }
  
  .save-button {
    background-color: #007bff;
    color: white;
  }
  
  .delete-button {
    background-color: #dc3545;
    color: white;
  }
  
  .remove-button {
    background-color: #dc3545;
    color: white;
  }
  
  .edit-button {
    background-color: #ffc107;
    color: black;
  }
  
  .move-button {
    background-color: #ffc107;
    color: black;
  }
  
  .process-button {
    background-color: #28a745;
    color: white;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  