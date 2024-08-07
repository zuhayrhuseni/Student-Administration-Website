<template v-if="isAuthenticated">
  <div>
    <header class="app-header">
      <div class="header-content">
        <h1>Select Subject to View Courses</h1>
      </div>
      <div class="divider"></div>
    </header>
    <div v-for="(subject, index) in subjects" :key="index" class="subject-row">
      <div class="subject-title" @click="selectSubject(index)">
        {{ Object.keys(subject)[0] }} {{ selectedSubject === index ? '▲' : '▼' }}
      </div>
      <div v-if="selectedSubject === index" class="courses-list">
        <h4 class="courses-header">Courses for {{ Object.keys(subject)[0] }}:</h4>
        <ul>
          <template v-if="Object.values(subject)[0].length === 0">
            <li class="course-info">None listed</li>
          </template>
          <template v-else>
            <li v-for="(course, courseIndex) in Object.values(subject)[0]" :key="courseIndex">
              <div class="course-info">
                <span class="course-id">{{ course.courseid }}</span>
                <span class="course-name">{{ course.name }}</span>
              </div>
              <div class="course-details">
                <p><strong>Description:</strong> {{ course.description }}</p>
                <p v-if="course.prereqs && course.prereqs.length">
                  <strong>Prerequisites: </strong>
                  <span v-for="(prereq, prereqIndex) in course.prereqs" :key="prereqIndex">
                    {{ prereq }}{{ prereqIndex < course.prereqs.length - 1 ? ', ' : '' }}
                  </span>
                </p>
                <p v-else>
                  <strong>Prerequisites: </strong>
                  <span>None</span>
                </p>
                <div class="indented-box">
                  <p class="list-sections" @click="fetchSections(index, courseIndex, course.courseid)">
                    <strong>List Sections {{ isSelectedCourse(index, courseIndex) ? '▲' : '▼' }}</strong>
                  </p>
                  <div v-if="isSelectedCourse(index, courseIndex)">
                    <template v-if="savedsections[course.courseid] && savedsections[course.courseid].length > 0">
                      <li v-for="(section) in savedsections[course.courseid]" :key="section.Section" class="section-item">
                        <div class="section-info">
                          <div class="section-number" @click="enrollCourse(course.courseid, section.Section, index, courseIndex)">
                            Section {{ section.Section }}
                          </div>
                          <div class="section-details">
                            <p><strong>Enrollment:</strong> {{ section.Enrollment }}</p>
                            <p><strong>Capacity:</strong> {{ section.Capacity }}</p>
                            <p><strong>Location:</strong> {{ section.Location }}</p>
                            <p><strong>Teacher Name:</strong> {{ section.TeacherName }}</p>
                            <div class="schedule">
                              <strong>Schedule:</strong>
                              <ul>
                                <li v-for="(value, day) in section.Schedule" :key="day">
                                  <span>{{ day }}:</span> {{ value }}
                                </li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </li>
                    </template>
                    <template v-else>No sections available.</template>
                  </div>
                </div>
              </div>
            </li>
          </template>
        </ul>
      </div>
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

//selectedSubject to track which subject is dropped down
const selectedSubject = ref(null);
//subjects to list
const subjects = ref([]);
//save which course drop downs have been opened for viewing sections
const selectedCourses = ref([]);
//keep track of sections that have been fetched - to save from spamming API calls
const savedsections = ref({});

//Auth0, router
const { isAuthenticated, user } = useAuth0();
const router = useRouter();

//data from auth0 to be used in API
let userID = '';
let role = null;

//API call to get a full list of offered courses - sorted by subject
const fetchSubjectTable = () => {
  const endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search';

  fetch(endpoint, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    if (data.statusCode === 200) { //if successful, store data
      subjects.value = data.body;
      selectedCourses.value = new Array(subjects.value.length).fill(null);
    }
  })
  .catch(error => {
    console.error('An error has occurred: ', error);
  });
};

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
    if (role != 'Student' || !isAuthenticated) {
        router.push('/not-authorized');
        return;
    }
    //start page
    fetchSubjectTable()
  }
}, { immediate: true });

//used to select a subject to drop down, closes other subjects
const selectSubject = (index) => {
  selectedSubject.value = selectedSubject.value === index ? null : index;
};

//selects different course-section drop downs
const selectCourse = (subjectIndex, courseIndex) => {
  selectedCourses.value[subjectIndex] = selectedCourses.value[subjectIndex] === courseIndex ? null : courseIndex;
};

//API call to get sections for a chosen course
const fetchSections = (subjectIndex, courseIndex, courseid) => {
  //call selectCourse method to toggle drop down
  selectCourse(subjectIndex, courseIndex);

  //checks if the sections for course have yet to be fetched
  if (!savedsections.value[courseid]) {
    savedsections.value[courseid] = [];
    let endpoint = `https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search/courses/sections?CourseID=${courseid}`;
    fetch(endpoint, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
      if (data.statusCode === 200) {
        //console.log(data.body)
        //store data in dictionary
        savedsections.value[courseid] = data.body;
      }
    })
    .catch(error => {
      console.error('An error has occurred: ', error);
    });
  }
};

//check if course is selected for drop down - tracks when subj drop down is closed
const isSelectedCourse = (subjectIndex, courseIndex) => {
  return selectedCourses.value[subjectIndex] === courseIndex;
};

//API call to enroll in a selected section of a selected course
const enrollCourse = (courseID, section, subjectIndex, courseIndex) => {
  let endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search/courses/sections';
  fetch(endpoint, {
    method: 'POST',
    body: JSON.stringify({ //body data type must match Content-Type header
      "CourseID": courseID,
      "UserID": userID.nickname,
      "Section": section
    }),
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.statusCode === 200) {
      //reload sections to update
      delete savedsections.value[courseID];
      fetchSections(subjectIndex, courseIndex, courseID);
      //alert sucess
      window.alert(data.body);
    }
    else {
      //console.log(data.body);
      console.log(data.statusCode);
      //alert failure and reason - determined in lambda
      window.alert(`Enrollment failed: ${data.body}`);
    }
  })
  .catch(error => {
    console.error('An error has occurred: ', error);
  });
};

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

.course-search {
  margin-top: 1rem;
  padding: 0 2rem;
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

.subject-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
}

.subject-title {
  width: 100%;
  cursor: pointer;
  margin-left: 10px;
  font-size: 18px;
}

.courses-list {
  margin-top: 10px;
}

.courses-header {
  margin-left: 10px;
  font-size: 16px;
}

.course-info {
  display: flex;
  justify-content: space-between;
  margin-left: 20px;
  margin-bottom: 5px;
}

.course-id,
.course-name {
  font-weight: bold;
}

.course-details {
  margin-left: 60px;
}

.list-sections {
  margin-left: 30px;
  cursor: pointer;
  font-weight: bold;
}

.section-item {
  list-style-type: none;
  padding-left: 0;
  margin-top: 10px;
}

.section-info {
  display: flex;
  justify-content: space-between;
}

.section-number {
  font-weight: bold;
  margin-right: 10px;
  cursor: pointer;
  text-decoration: underline;
}

.section-number:hover::after {
  content: "Click to enroll";
  position: absolute;
  top: -25px;
  right: 0;
  background-color: #333;
  color: #fff;
  padding: 2px 5px;
  border-radius: 5px;
  white-space: nowrap;
  z-index: 1;
}

.section-details {
  flex-grow: 1;
}

.schedule {
  margin-top: 10px;
}

.schedule ul {
  list-style-type: none;
  padding: 0;
}

.schedule li {
  margin-left: 0;
  font-weight: bold;
}
</style>