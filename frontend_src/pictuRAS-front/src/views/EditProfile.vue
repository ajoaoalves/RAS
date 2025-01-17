<template>
  <div>
    <Navbar />
    <div class="profile-view">
      <div class="profile-card">
        <h1 class="title">PICTURAS</h1>
        <h2 class="profile-title">Editar o teu perfil</h2>

        <div class="profile-info">
          <div class="form-group">
            <label>Nome completo:</label>
            <input type="text" v-model="user.fullName" placeholder="Digite seu nome completo" />
          </div>

          <div class="form-group">
            <label>Nome de utilizador:</label>
            <input type="text" v-model="user.username" placeholder="Digite seu nome de utilizador" />
          </div>

          <div class="form-group">
            <label>E-mail:</label>
            <input type="email" v-model="user.email" placeholder="Digite seu e-mail" />
          </div>
        </div>

        <div class="button-group">
          <button class="save-btn" @click="saveProfile">Salvar alterações</button>
          <button class="cancel-btn" @click="cancelEdit">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';

export default {
  name: "EditProfileView",
  components: {
    Navbar
  },
  data() {
    return {
      user: {
        fullName: "",
        username: "",
        email: ""
      }
    };
  },
  methods: {
    saveProfile() {
      console.log("Perfil atualizado:", this.user);
      alert("Perfil atualizado com sucesso!");
      this.$router.push('/profile'); // Redireciona para a visualização do perfil
    },
    cancelEdit() {
      console.log("Edição cancelada.");
      alert("Edição cancelada.");
      this.$router.push('/profile'); // Volta para a página de perfil
    }
  }
};
</script>

<style scoped>
/* Centraliza a página e evita que saia da tela */
.profile-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  background-color: #dfe8f5; /* Azul claro */
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

/* Cartão de edição do perfil muito mais estreito */
.profile-card {
  background-color: #ffffff;
  padding: 25px;
  width: 35%; /* Reduzido significativamente */
  max-width: 320px; /* Mais compacto */
  border-radius: 15px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  color: #333;
}

/* Título principal */
.title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #003c8f;
  margin-bottom: 15px;
}

/* Subtítulo */
.profile-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Informações do perfil */
.profile-info {
  text-align: left;
  font-size: 1rem;
  background-color: #f9f9f9;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
}

/* Estilização dos formulários */
.form-group {
  margin-bottom: 12px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
  box-sizing: border-box;
}

/* Botões */
.button-group {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 15px;
}

.save-btn {
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
}

.cancel-btn {
  background-color: #d9534f;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
}

.save-btn:hover {
  background-color: #0056b3;
}

.cancel-btn:hover {
  background-color: #c9302c;
}

/* Ajuste responsivo */
@media (max-width: 768px) {
  .profile-card {
    width: 85%;
    padding: 20px;
  }

  .profile-info {
    font-size: 0.9rem;
    padding: 10px;
  }

  .save-btn, .cancel-btn {
    font-size: 0.85rem;
    padding: 8px 12px;
  }
}
</style>