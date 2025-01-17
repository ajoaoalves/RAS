<template>
    <div class="home-page">
      <Navbar />
      <header class="hero-section">
        <h1>Welcome to PICTURAS</h1>
        <p>Your one-stop solution for creative plans and tools.</p>
        <button class="cta-button" @click="explorePlans">Register New Account</button>
      </header>
      <section class="features-section">
        <h2>Why Choose PICTURAS?</h2>
        <ul class="features-list">
          <li>✔️ Easy to Use</li>
          <li>✔️ Affordable Plans</li>
          <li>✔️ Top-notch Tools</li>
          <li>✔️ Excellent Support</li>
        </ul>
      </section>
    </div>
  </template>
  
  <script>
  import Navbar from "../components/Navbar.vue";
  
  export default {
    name: "HomePage",
    components: {
      Navbar,
    },
    methods: {
      explorePlans() {
        this.$router.push("/register");
      },
    },
  };
  </script>
  
  <style scoped>
  .home-page {
    font-family: Arial, sans-serif;
  }
  
  .hero-section {
    text-align: center;
    padding: 50px 20px;
    background-color: #09008a;
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .hero-section h1 {
    font-size: 3rem;
    margin-bottom: 20px;
  }
  
  .hero-section p {
    font-size: 1.2rem;
    margin-bottom: 30px;
  }
  
  .cta-button {
    background-color: white;
    color: #09008a;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .cta-button:hover {
    background-color: #ffe4c4;
  }
  
  .features-section {
    text-align: center;
    padding: 40px 20px;
    background-color: #f9f9f9;
    color: #333;
  }
  
  .features-section h2 {
    font-size: 2rem;
    margin-bottom: 20px;
  }
  
  .features-list {
    list-style: none;
    padding: 0;
    font-size: 1.2rem;
    color: #333;
  }
  
  .features-list li {
    margin-bottom: 10px;
  }
  </style>
  