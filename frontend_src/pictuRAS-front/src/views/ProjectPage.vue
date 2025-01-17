<template>
    <div class="project-page">
      <Navbar />
      <div class="project-header">
        <h1>Manage Project: {{ projectName }}</h1>
      </div>
  
      <!-- Project Images Section -->
      <section class="project-images">
        <h2>Upload Images</h2>
        <input type="file" multiple @change="uploadImages" accept="image/*" />
        <p v-if="uploadError" class="error">{{ uploadError }}</p>
        <div class="image-list">
          <h3>Uploaded Images:</h3>
          <ul>
            <li v-for="(image, index) in projectImages" :key="index" class="image-item">
              <img :src="image.url" alt="Uploaded Image" />
              <button class="delete-button" @click="deleteImage(index)">Delete</button>
            </li>
          </ul>
        </div>
      </section>
  
      <!-- Project Tools Section -->
      <section class="project-tools">
        <h2>Manage Tools</h2>
        <div class="tools-container">
          <div class="available-tools">
            <h3>Available Tools</h3>
            <ul>
              <li v-for="tool in availableTools" :key="tool.id" class="tool-item">
                {{ tool.name }}
                <button class="add-button" @click="addTool(tool)">Add</button>
              </li>
            </ul>
          </div>
          <div class="selected-tools">
            <h3>Selected Tools</h3>
            <ul>
              <li v-for="(tool, index) in selectedTools" :key="tool.id" class="tool-item">
                {{ tool.name }}
                <button class="remove-button" @click="removeTool(index)">Remove</button>
                <button class="move-button" @click="moveToolUp(index)" :disabled="index === 0">↑</button>
                <button class="move-button" @click="moveToolDown(index)" :disabled="index === selectedTools.length - 1">↓</button>
              </li>
            </ul>
          </div>
        </div>
        <button
          class="process-button"
          @click="processImages"
          :disabled="!selectedTools.length || !projectImages.length"
        >
          Process Images
        </button>
      </section>
    </div>
  </template>
  
  <script>
  import Navbar from "../components/Navbar.vue";
  export default {
    name: "ProjectPage",
    components: {
        Navbar
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
          { id: 1, name: "Rotate" },
          { id: 2, name: "Crop" },
          { id: 3, name: "Resize" },
          { id: 4, name: "Adjust Brightness" },
        ],
        uploadError: "",
      };
    },
    methods: {
      uploadImages(event) {
        const files = Array.from(event.target.files);
        files.forEach((file) => {
          if (file.size <= 5 * 1024 * 1024) {
            const reader = new FileReader();
            reader.onload = () => {
              this.projectImages.push({ url: reader.result, file });
            };
            reader.readAsDataURL(file);
          } else {
            this.uploadError = "Some files exceed the 5MB limit and were skipped.";
          }
        });
      },
      deleteImage(index) {
        this.projectImages.splice(index, 1);
      },
      addTool(tool) {
        if (!this.selectedTools.some((t) => t.id === tool.id)) {
          this.selectedTools.push({ ...tool });
        }
      },
      removeTool(index) {
        this.selectedTools.splice(index, 1);
      },
      moveToolUp(index) {
        if (index > 0) {
          const temp = this.selectedTools[index];
          this.selectedTools[index] = this.selectedTools[index - 1];
          this.selectedTools[index - 1] = temp;
        }
      },
      moveToolDown(index) {
        if (index < this.selectedTools.length - 1) {
          const temp = this.selectedTools[index];
          this.selectedTools[index] = this.selectedTools[index + 1];
          this.selectedTools[index + 1] = temp;
        }
      },
      processImages() {
        const processingRequest = {
          projectId: this.projectId,
          tools: this.selectedTools,
          images: this.projectImages.map((img) => img.file),
        };
        console.log("Processing Images Request: ", processingRequest);
      },
    },
  };
  </script>
  
  <style scoped>
  .project-page {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    padding: 20px;
    min-height: 100vh;
    color: #333;
  }
  
  .project-header {
    text-align: center;
    margin-bottom: 20px;
    background-color: #007bff;
    color: white;
    padding: 15px;
    border-radius: 8px;
  }
  
  .project-header h1 {
    margin: 0;
    font-size: 2rem;
  }
  
  .project-images,
  .project-tools {
    margin-bottom: 30px;
  }
  
  .project-images h2,
  .project-tools h2 {
    font-size: 1.5rem;
    margin-bottom: 10px;
  }
  
  .image-list ul {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .image-item img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 4px;
  }
  
  button {
    padding: 5px 10px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    transform: scale(1.05);
  }
  
  .add-button {
    background-color: #28a745;
    color: white;
  }
  
  .remove-button,
  .delete-button {
    background-color: #dc3545;
    color: white;
  }
  
  .move-button {
    background-color: #ffc107;
    color: black;
  }
  
  .process-button {
    background-color: #007bff;
    color: white;
    margin-top: 20px;
  }
  
  button:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
  }
  
  .tools-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  </style>
  