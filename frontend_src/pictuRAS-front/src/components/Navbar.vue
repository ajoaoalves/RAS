<template>
    <nav class="navbar">
      <div class="navbar-container">
        <a href="/" class="navbar-logo">PICTURAS</a>
        <ul class="navbar-links">
          <li><a href="/" class="navbar-link">Home</a></li>
          <li><a href="/plans" class="navbar-link">Plans</a></li>
          <li><a href="/about" class="navbar-link">About</a></li>
          <li><a href="/contact" class="navbar-link">Contact</a></li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "Navbar",
  };
  </script>
  
  <style scoped>
  .navbar {
    position: fixed; /* Make the navbar stick to the top */
    top: 0;
    left: 0;
    width: 100%; /* Full width */
    background-color: #ff7f50;
    color: white;
    padding: 15px 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1000; /* Ensure it stays above other elements */
  }
  
  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px; /* Optional: Center content within a container */
    margin: 0 auto;
  }
  
  .navbar-logo {
    font-size: 1.8rem;
    font-weight: bold;
    text-transform: uppercase;
    text-decoration: none;
    color: white;
  }
  
  .navbar-links {
    list-style: none;
    display: flex;
    gap: 20px;
    margin: 0;
    padding: 0;
  }
  
  .navbar-link {
    text-decoration: none;
    color: white;
    font-size: 1rem;
    transition: color 0.3s ease;
  }
  
  .navbar-link:hover {
    color: #ff4500;
  }
  </style>
  