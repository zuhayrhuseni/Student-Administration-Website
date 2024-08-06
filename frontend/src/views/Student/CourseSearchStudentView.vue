<template>
  <div>
    <header class="app-header">
      <div class="header-content">
        <h1>Select Subject to View Courses</h1>
      </div>
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

<script>


export default {
  props: ['user'],
  data() {
    return {
      selectedSubject: null,
      subjects: [],
      selectedCourses: [],  // Use an array to keep track of selected courses for each subject
      savedsections: {},    //array to keep track of fetched sections
    };
  },
  created() {
    // Call your API function here
    this.fetchSubjectTable();
  },
  methods: {
    fetchSubjectTable() {
      const endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search';
  
      fetch(endpoint, {
        method: 'GET',
      })
      .then(response => response.json())
      .then(data => {
        if (data.statusCode == 200) {
          this.subjects = data.body;
          this.selectedCourses = new Array(this.subjects.length).fill(null);
        }
      })
      .catch(error => {
        console.error('An error has occurred: ', error);
      });
    },
    selectSubject(index) {
      this.selectedSubject = this.selectedSubject === index ? null : index;
    },
    selectCourse(subjectIndex, courseIndex) {
      this.selectedCourses[subjectIndex] =
        this.selectedCourses[subjectIndex] === courseIndex ? null : courseIndex;
    },
    fetchSections(subjectIndex, courseIndex, courseid) {
      // Call selectCourse method to toggle course selection
      this.selectCourse(subjectIndex, courseIndex);

      //checks if the sections for course have yet to be fetched
      if (!this.savedsections[courseid]) {
        this.savedsections[courseid] = []
        let endpoint = `https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search/courses/sections?CourseID=${courseid}`;
        fetch(endpoint, {
          method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
          if (data.statusCode == 200) {
            console.log(data.body)
            this.savedsections[courseid] = data.body
          }
        })
        .catch(error => {
          console.error('An error has occurred: ', error);
        });
      }
    },
    isSelectedCourse(subjectIndex, courseIndex) {
      return this.selectedCourses[subjectIndex] === courseIndex;
    },
    enrollCourse(courseID, section, subjectIndex, courseIndex) {
      let endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/studenthomepage/search/courses/sections';
      fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify({
          "CourseID": courseID,
          "UserID": this.user,
          "Section": section
        }),
        headers: {
          'Content-Type': 'application/json'
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.statusCode == 200) {
          console.log(data.body)
          //reload sections
          delete this.savedsections[courseID]
          this.fetchSections(subjectIndex, courseIndex, courseID)
          window.alert(data.body)
        }
        else {
          console.log(data.body)
          console.log(data.statusCode)
          window.alert(`Enrollment failed: ${data.body}`)
        }
      })
      .catch(error => {
        console.error('An error has occurred: ', error);
      });
    }
  },
};
</script>

<style scoped>
/* General page styles */
body {
  font-family: 'Arial', sans-serif;
  color: #333;
  margin: 0;
  padding: 0;
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
  justify-content: space-between;
  align-items: center;
  font-size: 2rem;
  font-weight: bold;
}

/* Course search styles */
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

/* Subject row styles */
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