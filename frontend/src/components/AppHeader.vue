<template>
  <!-- Only render the app-header if showHeader is true -->
  <header v-if="showHeader" class="app-header">
    <div>
      <nav v-if="showLoginLink">
        <ul>
          <li>
            <logoutButton/>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink, useRoute } from "vue-router";
import { ref, watch } from 'vue';
import logoutButton from './buttons/logout-button.vue';

const title = ref("Section 1 Group 7 Course System");
const route = useRoute();

// by default, show the link and the header
const showLoginLink = ref(true);
const showHeader = ref(true); // new variable to control the header visibility

watch(route, (newRoute) => {
  // Hide the header and link only if on the home page
  const isHomePage = newRoute.path === '/home';
  showLoginLink.value = !isHomePage;
  showHeader.value = !isHomePage; // hide the entire header on the home page
});
</script>

<style>
.app-header {
  background-color: #007BFF; 
  border-bottom: 5px solid #fff;
  padding: 1rem;
  text-align: center;
}

.app-header a {
  color: #fff; 
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

.app-header a:hover {
  background-color: #FFC107; 
  color: #000; 
}
</style>
