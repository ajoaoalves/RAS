<template>
    <div class="login-view">
      <h1 class="title">PICTURAS</h1>
      <h2 class="subtitle">Login</h2>
  
      <div class="login-container">
        <LoginForm @submit-login="handleLogin" />
      </div>
    </div>
  </template>
  
  <script>
  import LoginForm from "../components/LoginForm.vue";
  
  export default {
    name: "LoginView",
    components: {
      LoginForm,
    },
    methods: {
      handleLogin(credentials) {
        // Simulación de autenticación
        const validEmail = "user@example.com";
        const validPassword = "password123";
  
        if (credentials.email === validEmail && credentials.password === validPassword) {
          alert("Login successful!");
        } else {
          alert("⚠️ Credenciais não correspondem a nenhum utilizador. Por favor tente de novo.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  .title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1e3a8a;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #374151;
    margin-bottom: 20px;
  }
  
  .login-container {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    width: 350px;
  }
  </style>
  