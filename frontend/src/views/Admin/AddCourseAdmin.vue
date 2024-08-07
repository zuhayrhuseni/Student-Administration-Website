<template v-if="isAuthenticated">
    <div>
      <header class="app-header">
        <div class="header-content">
          <h1>Type in the info for the section you would like to add!</h1>
        </div>
        <div class="divider"></div>
      </header>
      <div class="form-container">  
        <form @submit.prevent="addsection">
          <input v-model="course.CourseID" placeholder="Enter Course ID Here" />
          <input v-model="course.Capacity" placeholder="Enter Capacity Here" />
          <input v-model="course.Section" placeholder="Enter Section Number Here" />
          <input v-model="course.Location" placeholder="Enter Location Here" />
          <input v-model="course.Schedule" placeholder="Enter Schedule Here as a Map" />
          <input v-model="course.TeacherID" placeholder="Enter Teacher ID Here" />
          <input v-model="course.TeacherName" placeholder="Enter Teacher Name Here" />
          <button type="submit" class="submit-button">Add Section</button>
        </form>
    </div>
      <div class="banner-image">
        <img src="/uconn-banner.png" alt="UCONN Banner" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, nextTick } from 'vue';
  import { useAuth0 } from '@auth0/auth0-vue';
  import { useRouter } from "vue-router";
  
  //Auth0, router
  const { isAuthenticated, user } = useAuth0();
  const router = useRouter();
  //gets passed to html form
  const course = ref({
    CourseID: '',
    Capacity: '',
    Section: '',
    Location: '',
    Schedule: '',
    TeacherID: '',
    TeacherName: '',
  });

  let userID = '';
  let role = null;
  
  //watching for auth0 update - this is necessary to get user info and track authorization
  watch(user, async (newUser) => {   
    if (newUser && newUser.nickname) { 
      //store info and Role metadata
      userID = newUser;
      role = newUser['dev-75fp6aop37uung0c.us.auth0.com/Role'];
      //waiting here as a bug fix - originally would have to refresh page to have auth0 information show
      await nextTick();
      await new Promise(resolve => setTimeout(resolve, 0));
      //check page authorization
      if (role != 'Admin' || !isAuthenticated) {
          router.push('/not-authorized');
          return;
      }
    }
  }, { immediate: true });


  //function to parse schedule string into a map, easier for user to input
  function parseSchedule(scheduleStr) {
  const scheduleObj = {};
  const dayPairs = scheduleStr.split(', '); // split into day/time pairs
  dayPairs.forEach(pair => {
    const [day, timeRange] = pair.split(': ');
    scheduleObj[day.trim()] = { 'S': timeRange.trim() }; // add to schedule object
  });
  return scheduleObj;
}

  async function addsection() {
    console.log(course.value);
    let endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/adminhomepage/section';

    course.value.Capacity = parseInt(course.value.Capacity, 10); // convert to int
    course.value.Schedule = parseSchedule(course.value.Schedule); // convert to map using helper function

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(course.value), // body data type must match "Content-Type" header
        headers: {
          'Content-Type': 'application/json'
        },
      });

      const data = await response.json();
      if (response.ok) {
        // Handle success
        window.alert(`${data.body}`);
      } else {
        // Handle failure
        console.error(`Error: ${data.body}`);
        window.alert(`Error: ${data.body}`);
      }
    } catch (error) {
      console.error('An error has occurred: ', error);
      window.alert('Failed to add course');
    }
  }
  
  
  </script>
  
  <style scoped>
  body {
    font-family: 'Arial', sans-serif;
    color: #333;
    margin: 0;
    padding: 0;
  }
  
  .app-header {
    background-color: #005792;
    color: #fff;
    padding: 1rem 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 2rem;
    font-weight: bold;
  }

  .form-container form input {
    display: block;  
    margin-bottom: 1rem; 
    width: 100%; 
    box-sizing: border-box;  
    padding: 0.5rem;
    border: 5px solid #5b5b5b;
    border-radius: 1.5px;
    font-weight: bold;
    font-size: 1rem;
  }

  .form-container form .submit-button {
    background-color: #005792;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 10px;
  }

  .form-container form .submit-button:hover {
    background-color: #003f5c; 
  }

  </style>