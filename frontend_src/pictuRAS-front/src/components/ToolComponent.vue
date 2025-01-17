<template>
    <div class="tool-component">
      <h3>{{ tool.name }}</h3>
      <div v-if="parameters.length" class="parameters">
        <div
          v-for="param in parameters"
          :key="param.name"
          class="parameter-item"
        >
          <label :for="param.name">{{ param.label }}</label>
          <input
            v-if="param.type === 'number' || param.type === 'text'"
            :type="param.type"
            :id="param.name"
            :value="param.value"
            @input="updateParameter(param.name, $event.target.value)"
          />
          <select
            v-if="param.type === 'select'"
            :id="param.name"
            :value="param.value"
            @change="updateParameter(param.name, $event.target.value)"
          >
            <option v-for="option in param.options" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>
      <button @click="apply" class="apply-button">Apply</button>
    </div>
</template>
  
<script>
export default {
  name: "ToolComponent",
  props: {
    tool: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      parameters: this.initializeParameters(),
    };
  },
  methods: {
    initializeParameters() {
      if (this.tool.name === "Rotate") {
        return [{ name: "angle", label: "Angle (degrees)", type: "number", value: 0 }];
      } else if (this.tool.name === "Crop") {
        return [
          { name: "width", label: "Width (px)", type: "number", value: 100 },
          { name: "height", label: "Height (px)", type: "number", value: 100 },
        ];
      } else if (this.tool.name === "Resize") {
        return [{ name: "scale", label: "Scale (factor)", type: "number", value: 1 }];
      } else if (this.tool.name === "Adjust Brightness") {
        return [{ name: "brightness", label: "Brightness (%)", type: "number", value: 100 }];
      }
      // Default fallback
      console.warn(`No parameters defined for tool: ${this.tool.name}`);
      return [];
    },
    updateParameter(name, value) {
      const param = this.parameters.find((p) => p.name === name);
      if (param) param.value = value;
    },
    apply() {
      this.$emit("applyTool", {
        ...this.tool,
        parameters: this.parameters.reduce((acc, p) => {
          acc[p.name] = p.value;
          return acc;
        }, {}),
      });
    },
  },
};
</script>
  
  <style scoped>
  .tool-component {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    background-color: #fff;
    text-align: center;
  }
  
  .parameters {
    margin-top: 10px;
  }
  
  .parameter-item {
    margin-bottom: 10px;
  }
  
  .apply-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .apply-button:hover {
    background-color: #0056b3;
  }
  </style>
  