<template>
  <div>
    <Navbar />
    <div class="login-view">
      <h1 class="title">PICTURAS</h1>
      <h2 class="subtitle">Login</h2>

      <div class="login-container">
        <LoginForm @submit-login="handleLogin" />
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../stores/UserStore";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import LoginForm from "../components/LoginForm.vue";

export default {
  name: "LoginView",
  components: {
    LoginForm,
    Navbar,
  },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const handleLogin = (credentials) => {
      // Simulación de autenticación
      const validUsers = [
        { id: "1", name: "João Silva", email: "user@example.com", type: "admin" },
        { id: "2", name: "Maria Oliveira", email: "maria@email.com", type: "user" },
      ];

      const user = validUsers.find((u) => u.email === credentials.email);

      if (user && credentials.password === "password123") {
        userStore.setUser(user);
        alert("✅ Login successful!");
        router.push("/profile"); // Redirige al perfil después del login
      } else {
        alert("⚠️ Credenciais não correspondem a nenhum utilizador. Por favor tente de novo.");
      }
    };

    return { handleLogin };
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
  