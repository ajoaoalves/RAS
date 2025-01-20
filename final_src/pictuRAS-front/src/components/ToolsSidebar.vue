<template>
    <div class="sidebar">
      <h3>Ferramentas Básicas</h3>
      <div class="tools-section">
        <button class="tool-btn" v-for="tool in basicTools" :key="tool.name" @click="addTool(tool)">
          <i :class="tool.icon"></i>
          {{ tool.name }}
        </button>
      </div>
  
      <h3>Ferramentas Avançadas</h3>
      <div class="tools-section">
        <button class="tool-btn" v-for="tool in advancedTools" :key="tool.name" @click="addTool(tool)">
          <i :class="tool.icon"></i>
          {{ tool.name }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        basicTools: [
          { name: "Black/White", icon: "fas fa-adjust" },
          { name: "Resize", icon: "fas fa-expand" },
          { name: "Background Remover", icon: "fas fa-cut" },
          { name: "Grey Scale", icon: "fas fa-tint" },
          { name: "Rotation", icon: "fas fa-sync" },
          { name: "Brightness", icon: "fas fa-sun" }
        ],
        advancedTools: [
          { name: "People Counter", icon: "fas fa-users" },
          { name: "OCR", icon: "fas fa-file-alt" },
          { name: "Object Finder", icon: "fas fa-search" },
          { name: "Glasses Filter", icon: "fas fa-glasses" },
          { name: "Football Lines", icon: "fas fa-futbol" }
        ]
      };
    },
    methods: {
      addTool(tool) {
        this.$emit("tool-added", tool);
      }
    }
  };
  </script>
  
  <style scoped>
  .sidebar {
    padding: 20px;
    background-color: #d0e0f5;
    display: flex;
    flex-direction: column;
  }
  
  h3 {
    font-size: 16px;
    margin: 10px 0;
  }
  
  .tools-section {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  
  .tool-btn {
    background: white;
    border: none;
    padding: 10px;
    text-align: left;
    font-size: 14px;
    margin: 5px 0;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  
  .tool-btn i {
    margin-right: 10px;
  }
  </style>
  