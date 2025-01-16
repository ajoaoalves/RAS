<template>
    <div class="plan-card">
      <h2>{{ name }}</h2>
      <p>{{ description }}</p>
      <p class="price">{{ price }}</p>
      <button @click="handleClick">{{ buttonText }}</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "PlanCard",
    props: {
      name: {
        type: String,
        required: true,
      },
      description: {
        type: String,
        required: true,
      },
      price: {
        type: String,
        required: true,
      },
      buttonText: {
        type: String,
        required: true,
      },
      onClick: {
        type: Function,
        required: true,
      },
    },
    methods: {
      handleClick() {
        this.onClick();
      },
    },
  };
  </script>
  
  <style scoped>
  .plan-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    width: 300px;
    text-align: center;
    background-color: #f9f9f9;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .plan-card h2 {
    margin: 0 0 10px;
  }
  
  .plan-card .price {
    font-size: 1.5em;
    color: #333;
    margin: 15px 0;
  }
  
  button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  