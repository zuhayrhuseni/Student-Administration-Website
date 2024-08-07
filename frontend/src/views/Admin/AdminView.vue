<template v-if="isAuthenticated">
    <header class="app-header">
      <div class="header-content">
        <h1>Welcome {{ Name }}!</h1>
      </div>
      <div class="admin-header-content">
        <h1>{{ title }}</h1>
        <div class="load-subjects">
          <button @click="fetchSubjects">Load Subjects and Courses</button> 
        </div>
        <div class="router-link">
          <RouterLink to="/addcourseadmin">Add Course to Database</RouterLink>
        </div>
      </div>
      <div class="divider"></div>
    </header>
    <div class="subjects-container" v-if="loaded">
      <div v-for="(courses, subject) in subjects" :key="subject" class="subject">
        <h2>{{ "Subject: " + subject }}</h2>
        <ul v-if="courses.length">
          <li v-for="course in courses" :key="course.courseid">
            {{ course.courseid.S }} - {{ course.Name.S }}
          </li>
        </ul>
        <p v-else>No courses available for this subject</p>
      </div>
    </div>
    <div class="banner-image">
      <img src="/uconn-banner.png" alt="UCONN Banner" />
    </div>
  </template>
  
  
  
  <script setup>
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

const { isAuthenticated, user } = useAuth0(); 
const router = useRouter(); 
const subjects = ref({}); // Subjects and courses will be stored here
const loaded = ref(false); // set to true after subjects are loaded
const title = ref(''); 
let role = '';
let Name = ''

watch(user, async (newUser) => {
  if (newUser) {
    role = newUser['dev-75fp6aop37uung0c.us.auth0.com/Role']; // get role from Auth0 (student, teacher, or admin)
    Name = newUser['dev-75fp6aop37uung0c.us.auth0.com/full_name']; // get name from Auth0

    if (role !== 'Admin' || !isAuthenticated.value) { //don't allow access if not admin, push to not authorized page
      router.push('/not-authorized');
      return;
    }

    // Load subjects after authentication and role verification
  }
}, { immediate: true });

  // Function to fetch subjects and courses from the Lambda function
  async function fetchSubjects() {
    try {
      const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/adminhomepage`, {
        method: 'GET' // lambda function is set up to handle GET requests
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json(); // read response body as JSON
      const data = JSON.parse(result.body); // parse the JSON string into an object
      subjects.value = data;
      loaded.value = true; 
    } catch (error) {
      console.error('An error occurred:', error);
    }
  }
  </script>
  
    
  <style>
  body {
    font-family: 'Arial', sans-serif;
    color: #333;
    margin: 0;
    padding: 0;
  }
  .app-header {
    color: #fff;
    padding: 1rem 2rem;
    box-shadow: 0 2px 4px;
    text-align: center;
  }
  .admin-header-content {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3rem;
    font-weight: bold;
  }
  .admin-header-content h1{
    margin-bottom: 50px;
  }
  .subjects-container {
    font-size: 1.5rem;
    text-align: center;
  }
  .subject {
    margin: 1rem auto; 
    max-width: 600px; 
    font-weight: bolder;
  }
  .subject h2 {
    font-size: 3rem;
  }
  .banner-image {
    display: flex;
    justify-content: center; 
  }
  .banner-image img {
    width: 100%;
    height: auto;
    display: block;
  }

  .load-subjects button {
    color: #005792;
    text-decoration: none;
    font-weight: bold;
    background-color: #fff;
    padding: 1rem 2rem;
    border-radius: 4px;
    font-size: 2.2rem;
    border: none;
    cursor: pointer;
    margin-right: 100px;
  }

  .load-subjects button:hover {
    background-color: gold;
  }

  .router-link a {
    color: #005792;
    text-decoration: none;
    font-weight: bold;
    background-color: #fff;
    padding: 1rem 2rem;
    border-radius: 4px;
    font-size: 2.75rem;
    border: none;
    cursor: pointer;
    margin-left: 100px;
}

.router-link a:hover {
  background-color: gold;
}
.admin-header-content h1 {
  margin-bottom: 150px;
}
  </style>