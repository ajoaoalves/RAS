<template>
    <div class="modal-overlay" v-if="visible">
      <div class="modal">
        <h2>Confirm Deletion</h2>
        <p>Are you sure you want to delete "{{ projectName }}"?</p>
        <div class="modal-actions">
          <button @click="onConfirm" class="confirm-button">Yes, Delete</button>
          <button @click="onCancel" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ConfirmationModal",
    props: {
      visible: {
        type: Boolean,
        required: true,
      },
      projectName: {
        type: String,
        required: true,
      },
    },
    methods: {
      onConfirm() {
        this.$emit("confirm");
      },
      onCancel() {
        this.$emit("cancel");
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    color: #333;
}

  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  .modal-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  
  .confirm-button {
    background-color: #dc3545;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .cancel-button {
    background-color: #6c757d;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .confirm-button:hover {
    background-color: #c82333;
  }
  
  .cancel-button:hover {
    background-color: #5a6268;
  }
  </style>
  

  