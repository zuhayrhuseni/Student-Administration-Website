<template v-if="isAuthenticated">
  <header class="app-header">
    <div class="header-content">
      <h1>Welcome {{ Name }}!</h1>
      <div class="course-search">
        <RouterLink to="/studentcs">Course Search</RouterLink>
      </div>
    </div>
    <div class="divider"></div>
    <div class="course-list">
    <h2>Below are your enrolled courses:</h2>
    <ul>
      <li v-for="course in courses" :key="course" class="course-item">
        <span class="course-name">{{ course }}</span>
        <div class="course-info" v-if="courseInfo[course]">
          <ul>
            <li v-if="courseInfo[course].Location">
            <h4>Location:</h4> {{ courseInfo[course].Location }}
            </li>
            <br />
            <li v-if="courseInfo[course].TeacherName">
              <h4>TeacherName:</h4> {{ courseInfo[course].TeacherName }}
            </li>
            <li v-if="courseInfo[course].Schedule">
              <br />
              <h4>
              Schedule:
            </h4>
              <ul>
                <li v-for="(time, day) in courseInfo[course].Schedule" :key="day">
                  {{ day }}: {{ time }}
                </li>
              </ul>
            </li>
          </ul>
        </div>
        <button @click="dropCourse(course)">Drop</button>
      </li>
    </ul>
  </div>
  </header>
  <div class="banner-image">
    <img src="/uconn-banner.png" alt="UCONN Banner" />
  </div>
</template>
  
<script setup>
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, watch, nextTick } from "vue";
import { RouterLink, useRouter } from "vue-router";

//Auth0, router, course list
const { isAuthenticated, user } = useAuth0();
const router = useRouter();
const courses = ref([]);
const courseInfo = ref({});


//info from Auth0
let userID = '';
let role = null;
let Name = '';

//watching for auth0 update - this is necessary to get user info and track authorization
watch(user, async (newUser) => {   
  if (newUser && newUser.nickname) { 
    //store info and Role metadata
    userID = newUser;
    role = newUser['dev-75fp6aop37uung0c.us.auth0.com/Role'];
    Name = newUser['dev-75fp6aop37uung0c.us.auth0.com/full_name'];
    //waiting here as a bug fix - originally would have to refresh page to have auth0 information show
    await nextTick();
    await new Promise(resolve => setTimeout(resolve, 0));
    //check page authorization
    if (role != 'Student' || !isAuthenticated) {
        router.push('/not-authorized');
        return;
    }
    //start page
    listCourses();
  }
}, { immediate: true });

//API call to get list of enrolled courses
function listCourses() {
  if (userID && userID.nickname) { // check if user is valid
    let endpoint = `https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment?UserID=${userID.nickname}`;
    fetch(endpoint)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.statusCode == '200') {
          console.log(data.body);
          courses.value = data.body;

          // Automatically call getCourseInfo for each course
          courses.value.forEach(course => {
            getCourseInfo(course);
          });
        }
        else {
          console.log(data.body);
          window.alert(data.body);
        }
      })
      .catch(error => {
        console.error('An error occurred:', error);
      });
  }
}

//API call to drop a selected course
async function dropCourse(courseId) {
  try {
    const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'course_id_section': courseId,
        'UserID': userID.nickname
      })
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data);
      listCourses(); // Refresh the course list
      //alert based on result - string passed from lambda
      alert(JSON.stringify(data.body, null, 2));
    } else {
      alert(JSON.stringify(data.body, null, 2));
      throw new Error(data);
    }
  } catch (error) {
    console.error('Error dropping course:', error);
  }
  listCourses() // refresh the course list
}

//API call to get more course information
async function getCourseInfo(courseIDSection) {
  try {
    const response = await fetch(`https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/enrollment/courseinfo?course-id-section=${courseIDSection}`, {
      method: 'GET'
    });

    const data = await response.json();

    if (response.ok) {
      // Store course info
      courseInfo.value[courseIDSection] = data.body;
    } else {
      throw new Error(data);
    }
  } catch (error) {
    console.error('Error fetching course info:', error);
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
  background-color: #005792;
  color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  font-size: 3rem;
  font-weight: bold;
}


.header-content h1 {
  color:#fff;
  text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
  margin-right: auto; 
}

.course-search {
  margin-bottom: 1rem;
}

.course-search a {
  color: #005792;
  text-decoration: none;
  font-weight: bold;
  background-color: #fff;
  padding: 1rem 2rem;
  border-radius: 4px;
  font-size: 2.5rem;
}
.course-item {
  background-color: #e0e0e0;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.course-name {
  font-size: 2.5rem;
  white-space: nowrap; 
  margin-right: auto; 
  font-weight: bolder;
}

.course-info {
  flex: 1; 
  display: flex; 
  justify-content: center; 
  flex-direction: column; 
  padding: 0 1rem;
  font-size: 1.25rem;
  font-weight: bold;
  width: 500px;
  margin: 0 auto;
}

.course-info h4 {
  font-size: 1.5rem;
}

.course-item button {
  background-color: #005792;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 2rem;
  margin-left: 12rem;
}

.course-item button:hover {
  background-color: #003d5b;
}


.course-list {
  margin-top: 1rem;
  padding: 0 .5rem;
}

.course-list h2 {
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.banner-image img {
  width: 100%;
  height: auto;
  display: block;
  margin: 1rem 0;
}


.divider {
  height: 6px; 
  background-color: #fff; 
  margin: 1rem -2rem; 
  width: 200%; 
}
</style>
