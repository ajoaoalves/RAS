<template>
    <div class="editor-container">
      <Navbar />
  
      <div class="content">
        <ToolsSidebar @tool-added="addTool" />
  
        <!-- Área de Edição -->
        <div class="editor-area">
          <div class="image-preview">
            <img :src="selectedImage" alt="Imagem em edição" class="main-image" v-if="selectedImage" />
            <div v-else class="placeholder">Nenhuma imagem selecionada</div>
          </div>
  
          <div class="tool-bar">
            <div class="active-tools">
              <div v-for="(tool, index) in activeTools" :key="index" class="active-tool">
                <span>{{ tool.name }}</span>
                <button class="remove-btn" @click="removeTool(index)">✖</button>
              </div>
              <div class="add-tool-placeholder">Clique numa ferramenta para adicionar</div>
            </div>
          </div>
        </div>
  
        <!-- Sidebar Direita -->
        <div class="sidebar-right">
          <div class="image-thumbnails">
            <div v-for="(image, index) in images" :key="index" class="thumbnail">
              <img :src="image" alt="Miniatura" @click="selectImage(image)" />
              <button class="remove-btn" @click="removeImage(index)">✖</button>
            </div>
            <div class="add-image" @click="addImage">+</div>
          </div>
        </div>
      </div>
  
      <!-- Rodapé -->
      <div class="footer">
        <button class="process-btn" @click="processAll">Processar todas</button>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from "../components/Navbar.vue";
  import ToolsSidebar from "../components/ToolsSidebar.vue";
  
  export default {
    components: {
      Navbar,
      ToolsSidebar
    },
    data() {
      return {
        images: ["https://via.placeholder.com/100"],
        selectedImage: null,
        activeTools: []
      };
    },
    methods: {
      addTool(tool) {
        if (!this.activeTools.find(t => t.name === tool.name)) {
          this.activeTools.push(tool);
        }
      },
      removeTool(index) {
        this.activeTools.splice(index, 1);
      },
      selectImage(image) {
        this.selectedImage = image;
      },
      removeImage(index) {
        this.images.splice(index, 1);
        if (this.images.length === 0) {
          this.selectedImage = null;
        }
      },
      addImage() {
        const newImage = "https://via.placeholder.com/100";
        this.images.push(newImage);
      },
      processAll() {
        alert("Processando todas as imagens...");
      }
    }
  };
  </script>
  
  <style scoped>
  /* Layout principal */
  .editor-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #e6eff9;
    padding-top: 60px;
  }
  
  .content {
    display: grid;
    grid-template-columns: 250px auto 200px;
    flex-grow: 1;
  }
  
  /* Área de edição */
  .editor-area {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  
  .image-preview {
    width: 80%;
    height: 60%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }
  
  /* Sidebar direita */
  .sidebar-right {
    padding: 20px;
    background-color: #d0e0f5;
  }
  
  .footer {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }
  
  .process-btn {
    background: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
  }
  </style>
  
  