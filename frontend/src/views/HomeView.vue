<template>
  <header class="home-header">
    <div>
      <h1>{{ "Section 1 Group 7 Course System" }}</h1>
    </div>
  </header>
  <main class="home">
    <div class="login-section">
      <h2>Welcome to the Course Portal</h2>
      <div>
        <loginButton/>
      </div>
    </div>
  </main>
</template>

<script setup>
import loginButton from '../components/buttons/login-button.vue';
</script>

<style>
.home {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  height: 100vh;
  padding: 1rem;
  background-image: url('/UConnImage.jpeg');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
}

.login-section {
  text-align: center;
  padding: 1rem;
  padding-top: -100%;
}

.login-section h2 {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
}

.home-header {
  background-color: #007BFF;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem;
  text-align: center;
}

.home-header h1 {
  font-size: 2rem;
  font-weight: bold;
}
</style>
