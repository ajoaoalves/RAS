<template>
  <div>
    <Navbar />
    <div class="profile-view">
      <div class="profile-card">
        <h1 class="title">PICTURAS</h1>
        <h2 class="profile-title">O teu perfil</h2>

        <div class="profile-info" v-if="user">
          <p><strong>Nome completo:</strong><br> {{ user.name }}</p>
          <p><strong>Nome de utilizador:</strong><br> {{ username }}</p>
          <p><strong>E-mail:</strong><br> {{ user.email }}</p>
        </div>

        <div class="button-group">
          <button class="edit-btn" @click="editProfile">Editar perfil</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../stores/UserStore";
import { computed } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";

export default {
  name: "ProfileView",
  components: { Navbar },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    // Computed para obtener datos del usuario
    const user = computed(() => userStore.user);
    const username = computed(() => userStore.user.email.split("@")[0]); // Genera el nombre de usuario

    const editProfile = () => {
      console.log("Redirigindo para edição do perfil...");
      router.push("/edit-profile");
    };

    return { user, username, editProfile };
  },
};
</script>
  
  <style scoped>
  /* Asegurar que la vista cubra toda la pantalla sin barras de desplazamiento */
  .profile-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 95vh;
    width: 100vh;
    overflow: hidden;
    padding: 20px;
    box-sizing: border-box;
  }
  
  /* Tarjeta del perfil más compacta y centrada */
  .profile-card {
    background-color: #ffffff;
    padding: 30px;
    width: 50%;
    max-width: 450px; /* Tamaño óptimo para evitar barras */
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color: #333;
  }
  
  /* Título principal */
  .title {
    font-size: 2.2rem;
    font-weight: bold;
    color: #003c8f;
    margin-bottom: 15px;
  }
  
  /* Título del perfil */
  .profile-title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  /* Información del perfil */
  .profile-info {
    text-align: center;
    font-size: 1.2rem;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
    width: 100%;
    box-sizing: border-box;
  }
  
  /* Espaciado entre el nombre del atributo y el valor */
  .profile-info p {
    margin: 15px 0;
    font-size: 1.1rem;
    line-height: 1.6;
  }
  
  /* Botón Editar */
  .button-group {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .edit-btn {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
  }
  
  .edit-btn:hover {
    background-color: #0056b3;
  }
  
  /* Ajustes responsivos */
  @media (max-width: 768px) {
    .profile-card {
      width: 85%;
      padding: 25px;
    }
  
    .profile-info {
      font-size: 1rem;
      padding: 15px;
    }
  
    .edit-btn {
      font-size: 0.9rem;
      padding: 10px 15px;
    }
  }
  </style>
  