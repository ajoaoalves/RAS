<template>
    <div class="tool-component">
      <h3>{{ tool.name }}</h3>
      <div v-if="tool.parameters.length" class="parameters">
        <div
          v-for="param in tool.parameters"
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
  methods: {
    updateParameter(name, value) {
      const param = this.tool.parameters.find((p) => p.name === name);
      if (param) param.value = value;
    },
    apply() {
      this.$emit("applyTool", {
        ...this.tool,
        parameters: this.tool.parameters.reduce((acc, p) => {
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
  