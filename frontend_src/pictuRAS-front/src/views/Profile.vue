<template>
    <div>
      <Navbar />
      <div class="profile-view">
        <h1 class="title">PICTURAS</h1>
  
        <div class="profile-container">
          <div class="profile-card">
            <div class="profile-header">
              <i class="fas fa-user-circle"></i>
              <h2>O teu perfil</h2>
            </div>
  
            <div class="form-group">
              <label>Nome Completo:</label>
              <input type="text" v-model="user.fullName" placeholder="Nome Completo" />
            </div>
  
            <div class="form-group">
              <label>Nome de Utilizador:</label>
              <input type="text" v-model="user.username" placeholder="NomeDeUtilizador" />
            </div>
  
            <div class="form-group">
              <label>E-mail:</label>
              <input type="email" v-model="user.email" placeholder="example@email.com" />
            </div>
  
            <div class="form-group">
              <label>Palavra-passe:</label>
              <input type="password" v-model="user.password" placeholder="**********" />
            </div>
  
            <div class="button-group">
              <button class="save-btn" @click="saveProfile">Editar e Guardar</button>
              <button class="cancel-btn" @click="cancelEdit">Cancelar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from '../components/Navbar.vue';
  
  export default {
    name: "ProfileView",
    components: {
      Navbar
    },
    data() {
      return {
        user: {
          fullName: "",
          username: "",
          email: "",
          password: ""
        }
      };
    },
    methods: {
      saveProfile() {
        console.log("Perfil guardado:", this.user);
        alert("Perfil guardado com sucesso!");
      },
      cancelEdit() {
        console.log("Edição cancelada.");
        alert("Edição cancelada.");
      }
    }
  };
  </script>
  
  <style scoped>
  /* Centrar toda la vista */
  .profile-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Ocupar toda la altura de la pantalla */
    background-color: #dfe8f5; /* Fondo general */
  }
  
  /* Título principal */
  .title {
    font-size: 3rem;
    font-weight: bold;
    color: #003c8f;
    margin-bottom: 30px;
  }
  
  /* Contenedor para centrar la tarjeta */
  .profile-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  
  /* Tarjeta del perfil (más grande y con fondo azul) */
  .profile-card {
    background-color: #003c8f; /* Azul más intenso */
    padding: 40px;
    width: 60%; /* Más grande */
    max-width: 700px; /* Máximo tamaño */
    border-radius: 15px;
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
    text-align: center;
    color: white;
  }
  
  /* Encabezado de la tarjeta */
  .profile-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  /* Grupo de formularios */
  .form-group {
    text-align: left;
    margin-bottom: 15px;
  }
  
  /* Estilo de etiquetas */
  label {
    font-size: 1rem;
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
    color: white;
  }
  
  /* Estilo de los inputs */
  input {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    color: black;
  }
  
  /* Botones */
  .button-group {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }
  
  .save-btn {
    background-color: white;
    color: #003c8f;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
  }
  
  .cancel-btn {
    background-color: #d9534f;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
  }
  
  .save-btn:hover {
    background-color: #f0f0f0;
  }
  
  .cancel-btn:hover {
    background-color: #c9302c;
  }
  
  @media (max-width: 768px) {
    .profile-card {
      width: 90%;
      padding: 30px;
    }
  }
  </style>
  
  