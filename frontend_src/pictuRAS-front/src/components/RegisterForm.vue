<template>
    <form @submit.prevent="submitForm">
      <!-- Campo de Nome -->
      <div>
        <label for="name" class="label">Nome:</label>
        <input
          v-model="name"
          type="text"
          id="name"
          class="input-field"
          placeholder="Seu nome"
          required
        />
      </div>

      <!-- Campo de Username -->
      <div>
        <label for="username" class="label">Username:</label>
        <input
          v-model="username"
          type="username"
          id="username"
          class="input-field"
          placeholder="exemplo1234"
          required
        />
      </div>
  
      <!-- Campo de E-mail -->
      <div>
        <label for="email" class="label">E-mail:</label>
        <input
          v-model="email"
          type="email"
          id="email"
          class="input-field"
          placeholder="exemplo@email.com"
          required
        />
      </div>
  
      <!-- Campo de Senha -->
      <div>
        <label for="password" class="label">Senha:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          class="input-field"
          required
        />
      </div>
  
      <!-- Confirmar Senha -->
      <div>
        <label for="confirmPassword" class="label">Confirmar senha:</label>
        <input
          v-model="confirmPassword"
          type="password"
          id="confirmPassword"
          class="input-field"
          required
        />
      </div>
  
      <!-- Mensagem de Erro -->
      <p v-if="errorMessage" class="error-message">⚠️ {{ errorMessage }}</p>
  
      <!-- Botão de Registro -->
      <button type="submit" class="register-button">Registrar</button>
    </form>
</template>
  
<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
    };
  },
  methods: {
    submitForm() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "⚠️ As senhas não coincidem. Tente novamente.";
        return;
      }
      this.errorMessage = "";
      this.$emit("submit-register", {
        name: this.name,
        email: this.email,
        password: this.password,
        confirmPassword: this.confirmPassword,
      });
    },
  },
};
</script>
  
<style scoped>
.input-field {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.register-button {
  margin-top: 10px;
  background-color: #28a745;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-top: 5px;
}
</style>