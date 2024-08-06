<template>
  <header class="app-header">
  <div class="header-content">
    <h1>{{ title }}</h1>
    <div class="course-search">
      <RouterLink :to="{ name: 'studentcs', params: { user: username } }">Course Search</RouterLink>
    </div>
  </div>
    <div class="divider"></div>
    <div class="course-list">
      <h3>Below are your enrolled courses:</h3>
      <ul>
        <li v-for="course in courses" :key="course" class="course-item">
          {{ course }}
          <button @click="dropCourse(course)">Drop</button>
          <button @click="getCourseInfo(course)">Get Info</button>
        </li>
      </ul>
    </div>
  </header>
  <div class="banner-image">
      <img src="/uconn-banner.png" alt="UCONN Banner" />
    </div>
</template>


  
<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

const title = computed(() => `Welcome ${username.value}`);

const courses = ref([]); 

const route = useRoute(); 
const username = ref(route.query.userId); 

// Function to fetch courses from the API
function listCourses() {
  let userId = username.value;
  let endpoint = `https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment?UserID=${userId}`;

  console.log(endpoint);
  fetch(endpoint)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log(data.body);
      courses.value = data.body; // Assuming the Lambda function returns the data in the body attribute
    })
    .catch(error => {
      console.error('An error occurred:', error);
    });
}


// Call listCourses when the component is mounted
onMounted(() => {
  listCourses();
});

async function dropCourse(courseId) {
  try {
    const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'course_id_section': courseId,
        'UserID': username.value
      })
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data);
      listCourses(); // Refresh the course list
      alert(JSON.stringify(data.body, null, 2));
    } else {
      alert(JSON.stringify(data.body, null, 2));
      throw new Error(data);
    }
  } catch (error) {
    console.error('Error dropping course:', error);
  }
}

async function getCourseInfo(courseIdSection) {
  try {
    const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment/courseinfo?course-id-section=${courseIdSection}`, {
      method: 'GET'
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data.body);
      alert(JSON.stringify(data.body, null, 2)); // Display course info in a simple alert for now
    } else {
      throw new Error(data);
    }
  } catch (error) {
    console.error('Error fetching course info:', error);
  }
}

</script>

<style>
/* General page styles */
body {
  font-family: 'Arial', sans-serif;
  color: #333;
  margin: 0;
  padding: 0;
}

/* Header styles */

.header-content h1 {
  color:#fff;
  text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
}


/* Header styles */
.app-header {
  background-color: #005792;
  color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.header-content {
  display: flex;
  justify-content: space-between; /* Space between title and search */
  align-items: center;
  font-size: 3rem;
  font-weight: bold;
}

/* Course search styles */
.course-search {
  padding: 0 2rem;
  margin-bottom: 1rem;
}
.course-search a {
  color: #005792;
  text-decoration: none;
  font-weight: bold;
  background-color: #fff;
  padding: 1rem 2rem;
  border-radius: 4px;
  font-size: 1.5rem;
}


/* Course list styles */
.course-list {
  margin-top: 1rem;
  padding: 0 .5rem;
}
.course-list h3 {
  color: white;
  font-size: 1.75rem;
  font-weight: bold;
}
.course-item {
  background-color: #e0e0e0;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
}

.banner-image img {
  width: 100%; /* Set the width as needed */
  height: auto; /* Maintain aspect ratio */
  display: block; /* Remove any extra space below the image */
  margin: 1rem 0; /* Add some space around the image */
}

.divider {
  height: 4px; 
  background-color: #fff; 
  margin: 1rem -2rem; 
  width: 200%; 
}

</style>
