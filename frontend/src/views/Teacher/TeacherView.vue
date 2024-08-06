<template>
  <div>
    <header class="app-header">
      <div>
        <h1>{{ title }}</h1>
        <div>
          <h2>Here are the courses your are teaching this semester! Click "Get Info" for more information:</h2>
          <ul>
            <li v-for="course in courses" :key="course">
              {{ course }}
              <button @click="getCourseInfo(course)">Get Info</button>
            </li>
          </ul>
        </div>
      </div>
    </header>
    <div class="banner-image">
      <img src="/uconn-banner.png" alt="UCONN Banner" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const title = computed(() => `Welcome ${username.value}`);

const courses = ref([]); // This will hold the list of courses

const route = useRoute(); // Initialize the route here
const username = ref(route.query.userId); // Retrieve the passed username

// Function to fetch courses from the API
function listCourses() {
  let userId = username.value;
  let endpoint = `https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/teacherhomepage/enrollment?UserID=${userId}`;

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

async function getCourseInfo(courseIdSection) {
  try {
    const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/teacherhomepage/enrollment/courseinfo?course-id-section=${courseIdSection}`, {
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

<style scoped>
/* Styles can remain largely the same as your existing styles */
.app-header {
  background-color: #fcfcfc;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem;
}
.app-header h1 {
  font-size: 2rem;
  font-weight: bold;
}
.banner-image img {
  width: 100%; 
  height: auto;
  display: block;
  margin: 1rem 0;
}
</style>
