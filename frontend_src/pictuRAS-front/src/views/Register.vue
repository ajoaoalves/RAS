<template>
    <div class="register-view">
      <h1 class="title">PICTURAS</h1>
      <h2 class="subtitle">Registro</h2>
  
      <div class="register-container">
        <RegisterForm @submit-register="handleRegister" />
      </div>
    </div>
</template>
  
<script>
import RegisterForm from "../components/RegisterForm.vue";

export default {
  name: "RegisterView",
  components: {
    RegisterForm,
  },
  methods: {
    handleRegister(credentials) {
      if (credentials.password !== credentials.confirmPassword) {
        alert("⚠️ As senhas não coincidem. Tente novamente.");
        return;
      }
      alert("✅ Registro bem-sucedido para " + credentials.name);
    },
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
  background-color: #f4f4f4;
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