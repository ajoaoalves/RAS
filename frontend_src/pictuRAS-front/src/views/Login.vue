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
import axios from 'axios'; // Certifique-se de importar axios aqui
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

    const handleLogin = async (credentials) => {
      console.log("Credenciais enviadas:", credentials); // Log para verificar
      try {
        const response = await axios.post('/users/login', credentials); // Corrigido o URL
        console.log("Resposta do backend:", response.data); // Verifique a resposta
        const user = response.data;

        if (user) {
          userStore.setUser(user);
          console.log("Utilizador autenticado:", userStore.user);
          alert("✅ Login bem-sucedido!");
          router.push("/profile");
        } else {
          alert("⚠️ Credenciais não correspondem a nenhum utilizador. Por favor tente de novo.");
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("⚠️ Credenciais inválidas!");
        } else {
          alert("⚠️ Erro no servidor. Por favor, tente novamente.");
        }
        console.error("Erro no login:", error);
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