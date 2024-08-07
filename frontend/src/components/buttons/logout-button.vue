<!--this is copied from the lab9 Auth0 example-->

<template>
    <button class="button__logout" @click="handleLogout">Log Out</button>
  </template>
  
  <script setup>
  import { useAuth0 } from "@auth0/auth0-vue";
  
  const { logout } = useAuth0(); // this is the logout function from the Auth0 SDK
  
  // handleLogout function to handle the logout button click event
  const handleLogout = () => 
    logout({
      logoutParams: {
        returnTo: window.location.origin, // this is the URL that the user will be redirected to after logout
      }
    });
  </script>

<style>
.button__logout {
  background-color: #000000; 
  color: white; 
  padding: 15px 50px; 
  text-align: center; 
  text-decoration: none; 
  display: inline-block;
  font-size: 16px; 
  margin: 4px;
  cursor: pointer; 
  border: none; 
  border-radius: 10px; 
}

.button__logout:hover {
  background-color: #007BFF;
}
</style>