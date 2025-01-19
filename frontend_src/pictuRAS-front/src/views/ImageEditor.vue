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
            <div v-if="activeTools.length === 0" class="add-tool-placeholder">
              Clique numa ferramenta para adicionar
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar Direita -->
      <div class="sidebar-right">
        <div class="image-thumbnails">
          <div v-for="(image, index) in images" :key="index" class="thumbnail">
            <img :src="image" alt="Miniatura" @click="selectImage(image)" />
            <p class="thumbnail-text">Imagem {{ index + 1 }}</p>
            <button class="remove-btn small-remove-btn" @click="removeImage(index)">✖</button>
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
  grid-template-columns: 250px auto 250px;
  flex-grow: 1;
}

/* Área de edição */
.editor-area {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

/* Mantiene el tamaño fijo para evitar que la imagen se haga más pequeña */
.image-preview {
  width: 90%;
  height: 70vh;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  flex-shrink: 0; /* Evita que se reduzca cuando se agregan herramientas */
}

.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Lista de ferramentas ativas en columna */
.tool-bar {
  margin-top: 20px;
  width: 90%;
  max-height: 200px; /* Limita la expansión de herramientas */
  overflow-y: auto; /* Agrega scroll si hay muchas herramientas */
  display: flex;
  justify-content: center;
}

.active-tools {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.active-tool {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 180px;
}

.remove-btn {
  background-color: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.small-remove-btn {
  width: 16px;
  height: 16px;
  font-size: 10px;
}

/* Sidebar direita */
.sidebar-right {
  padding: 20px;
  background-color: #d0e0f5;
}

.image-thumbnails {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.thumbnail {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
}

.thumbnail img {
  width: 70px;
  height: 70px;
  cursor: pointer;
  border-radius: 5px;
  object-fit: contain;
}

.thumbnail-text {
  font-size: 14px;
  color: black;
  max-width: 100px;
  white-space: normal;
  overflow: hidden;
  text-align: center;
}

.thumbnail .remove-btn {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(50%, -50%);
}

.add-image {
  background-color: #007bff;
  color: white;
  font-size: 20px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  cursor: pointer;
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
