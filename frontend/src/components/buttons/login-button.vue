<!-- this is copied from the lab9 Auth0 example, styling is our own -->
<template>
  <button class="button__login" @click="handleLogin">Log In with Auth0</button>
</template>

<script setup>
import { useAuth0 } from "@auth0/auth0-vue";

const { loginWithRedirect } = useAuth0(); // useAuth0 hook to retrieve the loginWithRedirect method

// handleLogin function to handle the login button click event
const handleLogin = () => {
  loginWithRedirect({
    appState: {
      target: "/callback", // redirect to callback page after login
    },
  });
};
</script>

<style>
.button__login {
  background-color: #000000; 
  color: white; 
  padding: 15px 32px; 
  text-align: center; 
  text-decoration: none; 
  display: inline-block;
  font-size: 36px; 
  margin: 40px 2px; 
  cursor: pointer; 
  border: none; 
  border-radius: 10px; 
}

.button__login:hover {
  background-color: #007BFF; 
  box-shadow: 0 2px #666; 
}
</style>
