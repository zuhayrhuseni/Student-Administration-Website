<template>
  <!-- Only render the app-header if showHeader is true -->
  <header v-if="showHeader" class="app-header">
    <div>
      <nav v-if="showLoginLink">
        <ul>
          <li class="centered">
            <RouterLink to="/home" class="logout-button">Logout</RouterLink>
            <RouterLink v-if="$route.path.startsWith('/studentcs/')" :to="`/studenthome?userId=${$route.params.user}`" class="logout-button">Homepage</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink, useRoute } from "vue-router";
import { ref, watch } from 'vue';

const title = ref("Section 1 Group 7 Course System");
const route = useRoute();

// By default, show the link and the header
const showLoginLink = ref(true);
const showHeader = ref(true); // New variable to control the header visibility

watch(route, (newRoute) => {
  const isHomePage = newRoute.path === '/home';
  showLoginLink.value = !isHomePage;
  showHeader.value = !isHomePage; 
});
</script>

<style>
.app-header {
  background-color:#007BFF;
  border-bottom: 4px solid #fff;
  padding: 1rem;
  text-align: center;
}

/* Logout button styles */
.app-header a {
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

/* Highlight color on hover */
.app-header a:hover {
  background-color: #FFC107; 
  color: #000; 
}


.logout-button {
  font-size: 2rem; 
  padding: 1.5rem 2.5rem; 
  background-color: #007BFF; 
  font-weight: bold; 
  margin: 0.5rem;
  border: none;
}

.logout-button:hover {
  background-color: #FFC107;
  color: #000;
}
</style>
