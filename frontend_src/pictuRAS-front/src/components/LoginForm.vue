<template>
    <form @submit.prevent="submitForm">
      <!-- Campo de Email -->
      <div>
        <label for="email" class="label">E-mail ou nome de utilizador:</label>
        <input
          v-model="email"
          type="email"
          id="email"
          class="input-field"
          placeholder="example@email.com"
          required
        />
      </div>
  
      <!-- Campo de Contraseña -->
      <div class="mt-4">
        <label for="password" class="label">Palavra-passe:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          class="input-field"
          required
        />
      </div>
  
      <!-- Mensaje de Error -->
      <p v-if="errorMessage" class="error-message">
        ⚠️ Credenciais não correspondem a nenhum utilizador. Por favor tente de novo.
      </p>
  
      <!-- Botón de Login -->
      <button type="submit" class="login-button">➜</button>
    </form>
  </template>
  
  <script>
  export default {
    name: "LoginForm",
    data() {
      return {
        email: "",
        password: "",
        errorMessage: false,
      };
    },
    methods: {
      submitForm() {
        this.$emit("submit-login", {
          email: this.email,
          password: this.password,
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .label {
    display: block;
    font-size: 0.9rem;
    color: #374151;
    margin-bottom: 5px;
  }
  
  .input-field {
    width: 100%;
    padding: 10px;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    outline: none;
    transition: border-color 0.2s;
  }
  
  .input-field:focus {
    border-color: #3b82f6;
  }
  
  .error-message {
    color: #dc2626;
    font-size: 0.875rem;
    margin-top: 5px;
  }
  
  .login-button {
    width: 100%;
    margin-top: 15px;
    background-color: #2563eb;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.2rem;
  }
  
  .login-button:hover {
    background-color: #1e40af;
  }
  </style>
  