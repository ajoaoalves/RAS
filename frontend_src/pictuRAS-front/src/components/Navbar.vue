<template>
    <nav class="navbar" :class="{ hidden: !isNavbarVisible }">
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
    data() {
      return {
        isNavbarVisible: true,
        lastScrollPosition: 0,
        scrollThreshold: 50, // Minimum scroll distance to trigger visibility change
      };
    },
    methods: {
      handleScroll() {
        const currentScrollPosition = window.scrollY;
        const scrollDelta = currentScrollPosition - this.lastScrollPosition;
  
        if (Math.abs(scrollDelta) > this.scrollThreshold) {
          if (scrollDelta > 0) {
            // Scrolling down
            this.isNavbarVisible = false;
          } else {
            // Scrolling up
            this.isNavbarVisible = true;
          }
          this.lastScrollPosition = currentScrollPosition;
        }
      },
    },
    mounted() {
      window.addEventListener("scroll", this.handleScroll);
    },
    beforeDestroy() {
      window.removeEventListener("scroll", this.handleScroll);
    },
  };
  </script>
  
  <style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #ff7f50;
    color: white;
    padding: 15px 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transition: transform 0.3s ease; /* Smooth transition */
  }
  
  .navbar.hidden {
    transform: translateY(-100%); /* Slide out of view */
  }
  
  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
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
  