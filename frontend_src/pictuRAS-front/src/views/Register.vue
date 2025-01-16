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
}

.register-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
}
</style>
