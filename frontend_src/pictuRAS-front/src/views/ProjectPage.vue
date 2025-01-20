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
        <!-- Note: @change now calls our WebSocket-based logic -->
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
  <div class="tools-category">
    <h3>Basic Tools</h3>
    <div class="tools-grid">
      <ToolComponent
        v-for="tool in basicTools"
        :key="tool.name"
        :tool="tool"
        @applyTool="applyTool"
      />
    </div>
  </div>
  <div class="tools-category">
    <h3>Advanced Tools</h3>
    <div class="tools-grid">
      <ToolComponent
        v-for="tool in advancedTools"
        :key="tool.name"
        :tool="tool"
        @applyTool="applyTool"
      />
    </div>
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
      <!-- Use step.previewUrl if it exists, otherwise fallback to original image -->
      <img
        :src="step.previewUrl"
        :alt="`Preview Step ${stepIndex + 1}`"
        class="thumbnail"
        @click="openImage(step.previewUrl)"
      />
      <p>Step {{ stepIndex + 1 }}: {{ step.procedure }}</p>
    </div>
  </div>
  <p v-else>No image selected. Click on an image to view its preview.</p>
</section>        
<section class="result-section">
  <h2>Results</h2>
  <ul>
    <li v-for="(result, index) in results" :key="index">
      <h3>{{ result.type }}</h3>
      <p>
        <img :src="result.result" :alt="`Result ${index + 1}`" class="thumbnail" />
      </p>
    </li>
  </ul>
</section>

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
  import { io } from "socket.io-client";
  
  export default {
    name: "ProjectDashboard",
    components: { Navbar, ToolComponent },
    mounted() {
      this.fetchProjectData();
      const projectStore = useProjectStore();
      this.projectName = projectStore.project.name;
      this.projectId = projectStore.project.id;
      this.socket = io("http://localhost:8180");
      this.socket.on("image_data", this.handleImageData);
      this.socket.on("images_complete", this.handleImagesComplete);
      this.socket.on("ack", (data) => {
        console.log("Server acknowledgment:", data);
      // You can set a status message or handle UI updates here
        });
      this.socket.on('result', this.handleResult);
      this.socket.on('preview_update', this.handlePreviewUpdate);
      this.requestProjectImages();
    },
    data() {
      return {
        projectName: "",
        projectId: "",
        socket: null,
        projectImages: [],
        selectedTools: [],
        results: [],
        basicTools: [
        {
          name: "Border",
          procedure: "border",
          parameters: [
            { name: "bordersize", label: "Border Size (px)", type: "number", value: 1 },
            { name: "bordercolor", label: "Border Color (hex)", type: "text", value: "#000000" },
          ],
        },
        {
          name: "Crop",
          procedure: "crop",
          parameters: [
            { name: "left", label: "Left", type: "number", value: 0 },
            { name: "upper", label: "Upper", type: "number", value: 0 },
            { name: "right", label: "Right", type: "number", value: 100 },
            { name: "lower", label: "Lower", type: "number", value: 100 },
          ],
        },
        {
          name: "Rotation",
          procedure: "rotation",
          parameters: [{ name: "angle", label: "Angle (degrees)", type: "number", value: 0 }],
        },
        {
          name: "Brightness",
          procedure: "brightness",
          parameters: [{ name: "brightnessValue", label: "Brightness (factor)", type: "number", value: 1.0 }],
        },
        {
          name: "Binarization",
          procedure: "binarization",
          parameters: [], // No specific parameters mentioned
        },
        {
          name: "Resize",
          procedure: "resize",
          parameters: [
            { name: "width", label: "Width (px)", type: "number", value: 1920 },
            { name: "height", label: "Height (px)", type: "number", value: 1080 },
          ],
        },
      ],
      advancedTools: [
        {
          name: "Count People",
          procedure: "count-people",
          parameters: [], // No specific parameters mentioned
        },
        {
          name: "Object Detection",
          procedure: "object-detection",
          parameters: [], // No specific parameters mentioned
        },
        {
          name: "Background Removal",
          procedure: "background-removal",
          parameters: [], // No specific parameters mentioned
        },
        {
          name: "Watermark",
          procedure: "watermark",
          parameters: [],
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
        this.selectedTools = tools.map((tool) => ({
          ...tool,
          previewUrl: null, // initially, no preview
        }));
        console.log("Project data loaded successfully:", response.data);
      } catch (error) {
        console.error("Error loading project data:", error.message);
        alert("Failed to load project data. Please refresh the page.");
      }
    },
    requestProjectImages() {
      const projectStore = useProjectStore();
      if (!projectStore.project._id) {
        console.warn("No projectId found! Cannot request images.");
        return;
      }
      console.log("Requesting images for project:", projectStore.project._id);
      this.socket.emit("request_images", projectStore.project._id);
    },
    handleImageData({ projectId, contentType, binaryData }) {
      console.log(`Received image for project ID: ${projectId} with type: ${contentType}`);

      // Convert binary data to Blob and then to Object URL
      const blob = new Blob([binaryData], { type: contentType });
      const url = URL.createObjectURL(blob);

      // Example: If the server doesn't send a filename, you could store a generated name
      // or some ID. For demonstration, let's generate a unique name with a timestamp.
      const imageName = `project_${projectId}_${Date.now()}`;

      // Push into projectImages
      this.projectImages.push({
        name: imageName,
        url: url,
      });
    },
    handleResult({ imageData }) {
    console.log("Result:", imageData);
    console.log("Received result with type:", imageData.contentType);

    // Determine the correct MIME type
    let mimeType = imageData.contentType === "binary/octet" ? "image/jpeg" : imageData.contentType;

    try {
        // Convert binary data to Blob and then to Object URL
        const blob = new Blob([new Uint8Array(imageData.data)], { type: mimeType });
        const url = URL.createObjectURL(blob);

        // Push to results for rendering
        this.results.push({ type: "image", result: url });

        console.log("Image URL created:", url);
    } catch (error) {
        console.error("Error processing image data:", error);
    }
    },

    handlePreviewUpdate({ numTool, imageData }) {
    console.log(`Received preview update for tool ${numTool}.`);

    // Determine the correct MIME type
    let mimeType = imageData.contentType === "binary/octet" ? "image/jpeg" : imageData.contentType;

    try {
        // Convert binary data to Blob and then to Object URL
        const blob = new Blob([new Uint8Array(imageData.data)], { type: mimeType });
        const url = URL.createObjectURL(blob);

        // Update the preview URL for the corresponding tool
        this.selectedTools[numTool].previewUrl = url;

        console.log("Preview URL created:", url);
    } catch (error) {
        console.error("Error processing preview data:", error);
    }
    },
    

    handleImagesComplete({ message, projectId }) {
      console.log(`All images for project ID ${projectId} have been received. ${message}`);
    },
    uploadImages(event) {
      const projectStore = useProjectStore();
      const files = Array.from(event.target.files);
      files.forEach((file) => {
        // Enforce a 5MB limit for demo
        if (file.size <= 5 * 1024 * 1024) {
          // 1) Create a FileReader for the *binary* data
          const reader = new FileReader();
          reader.onload = () => {
            // Emit via socket: "image" event
            this.socket.emit("image", {
              projectId: projectStore.project._id,
              imageData: reader.result, // This is the ArrayBuffer
            });
            console.log("Uploaded image:", file.name);
            console.log("Project ID:", projectStore.project._id);

            // (Optional) For immediate local preview as base64
            const base64Reader = new FileReader();
            base64Reader.onload = () => {
              this.projectImages.push({
                url: base64Reader.result,
                name: file.name,
              });
            };
            // Convert the same file to base64 for local preview
            base64Reader.readAsDataURL(file);
          };
          // Read the file as ArrayBuffer for binary upload
          reader.readAsArrayBuffer(file);
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
        // id in string
        const formattedTool = {
    ...tool,
    // name of the tool and date
    _id: `${tool.procedure}-${Date.now()}`,
    parameters: Object.keys(tool.parameters || {}).map((key) => ({
      name: key,
      value: tool.parameters[key],
    })),
  };
  this.selectedTools.push(formattedTool);
        console.log("Applied tool:", formattedTool);
        console.log("Selected tools:", this.selectedTools);
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
        console.log("Tool edits saved successfully.");
        console.log("Selected tools:", this.selectedTools);
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
      async processImages() {
        console.log("Processing images with toolchain:", this.selectedTools);
        const projectStore = useProjectStore();
        const userStore = useUserStore();
        const projectData = {
            _id: projectStore.project._id,
            name: projectStore.project.name,
            user_id: userStore.user.id,
            tools: this.selectedTools.map(tool => ({
                _id: tool._id,
                procedure: tool.procedure,
                parameters: Array.isArray(tool.parameters)
                    ? tool.parameters.reduce((acc, param) => {
                            acc[param.name] = param.value;
                            return acc;
                        }, {})
                    : tool.parameters
            }))
        };
        try {
            const response = await axios.put(`/users/${userStore.user.id}/projects/${projectStore.project._id}/exec`, projectData);
            console.log("Project processed successfully:", response.data);
        } catch (error) {
            console.error("Error processing project:", error.message);
            alert("Failed to process project. Please try again.");
        }
          
      },
    async saveProject() {
        const userStore = useUserStore();
        const projectStore = useProjectStore();

        const projectData = {
            _id: projectStore.project._id,
            name: projectStore.project.name,
            user_id: userStore.user.id,
            tools: this.selectedTools.map(tool => ({
                _id: tool._id,
                procedure: tool.procedure,
                parameters: Array.isArray(tool.parameters)
                    ? tool.parameters.reduce((acc, param) => {
                            acc[param.name] = param.value;
                            return acc;
                        }, {})
                    : tool.parameters
            }))
        };

        try {
            const response = await axios.put(`/users/${userStore.user.id}/projects/${projectStore.project._id}`, projectData);
            console.log("Project saved successfully:", response.data);
        } catch (error) {
            console.error("Error saving project:", error.message);
            alert("Failed to save project. Please try again.");
        }
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

  .download-button {
  background-color: #17a2b8;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  text-decoration: none;
  display: inline-block;
  margin-top: 5px;
}

.download-button:hover {
  background-color: #138496;
}

  </style>
  