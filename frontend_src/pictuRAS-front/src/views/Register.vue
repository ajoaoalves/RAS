<template>
  <div>
    <Navbar />
    <div class="register-view">
      <h1 class="title">PICTURAS</h1>
      <h2 class="subtitle">Registro</h2>

      <div class="register-container">
        <RegisterForm @submit-register="handleRegister" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // Certifique-se de importar axios aqui
import { useUserStore } from "../stores/UserStore";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import RegisterForm from "../components/RegisterForm.vue";

export default {
  name: "RegisterView",
  components: {
    RegisterForm,
    Navbar,
  },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const handleRegister = async (credentials) => {
      // Verificar si las contraseñas coinciden
      if (credentials.password !== credentials.confirmPassword) {
        alert("⚠️ As senhas não coincidem. Tente novamente.");
        return;
      }

      // // Verificar si el usuario ya está registrado
      // if (userStore.user.email === credentials.email) {
      //   alert("⚠️ Este e-mail já está registrado.");
      //   return;
      // }

      try {
        const response = await axios.post('/users', credentials); // Corrigido o URL
        console.log("Resposta do backend:", response.data); // Verifique a resposta
        const user = response.data;

        if (user) {
          userStore.setUser(user);
          console.log("Utilizador autenticado:", userStore.user);
          alert("✅ Registo bem-sucedido!");
          router.push("/profile");
        } else {
          alert("⚠️ Credenciais más.");
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("⚠️ Credenciais inválidas!");
        } else {
          alert("⚠️ Erro no servidor. Por favor, tente novamente.");
        }
        console.error("Erro no registo:", error);
      }

      // Guardar el usuario en Pinia
      userStore.setUser({
        id: new Date().getTime().toString(), // Simulación de un ID único
        name: credentials.name,
        email: credentials.email,
        type: "user",
      });

      //alert("✅ Registro bem-sucedido!");
      router.push("/profile"); // Redirigir al perfil
    };

    return { handleRegister };
  },
};
</script>

  
<style scoped>
.register-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.register-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-field {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.register-button {
  margin-top: 10px;
  background-color: #28a745;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.error-message {
  color: red;
  margin-top: 5px;
  text-align: center;
}
</style>