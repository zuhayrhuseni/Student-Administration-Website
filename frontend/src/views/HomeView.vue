<template>
  <header class = "home-header">
    <div>
      <h1>{{ "Section 1 Group 7 Course System" }}</h1>
    </div>
  </header>
  <main class="home">
      <div class="login-section">
          <h2>Welcome to the Course Portal</h2>

          <div class="credentials">
              <input type="text" placeholder="Username" v-model="username">
              <input type="password" placeholder="Password" v-model="password">
          </div>

          <div class="login-options">
              <button @click="loginAs('Student')">Login as Student</button>
              <button @click="loginAs('Admin')">Login as Admin</button>
              <button @click="loginAs('Teacher')">Login as Teacher</button>
          </div>
      </div>
      <!-- For Login Failures -->
      <div class="modal" v-if="showModal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <!--<h3>Login Failed</h3>-->
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router"; // Import useRouter

const router = useRouter(); // Initialize the router
const username = ref("");
const password = ref("");

function loginAs(role) {
  let endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/login';

  fetch(endpoint, {
    method: 'POST',
    body: JSON.stringify({
      "UserID": username.value,
      "Type": role,
      "Password": password.value
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      return response.json();
    })
    .then(data => {
      if (data.statusCode === 200) {
        // Successful login
        console.log(data.body);

        // Redirect based on role
        if (role == 'Student') {
          // Use router.push with query parameters
          router.push({ path: '/studenthome', query: { userId: username.value } });
        } else if (role == 'Teacher') {
          router.push({ path: '/teacherhome', query: { userId: username.value } });;
        } else if (role == 'Admin') {
          router.push('/adminhome');
        }
      } else {
        // Login failure
        console.log(data.body);
        openModal(data.body);
      }
    })
    .catch(error => {
      console.error('An error occurred:', error);
    });
}

const showModal = ref(false);
const errorMessage = ref("");

function openModal(message) {
  errorMessage.value = message;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

</script>


<style>
.home {
  display: flex;
  align-items: flex-start; /* Align to the top of the container */
  justify-content: center;
  height: 100vh;
  padding: 1rem;
  
  /* Background image */
  background-image: url('/UConnImage.jpeg');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
}

.login-section {
  text-align: center;
  padding: 1rem;
  padding-top: 5%; /* You can adjust this value to your preference */
}

.login-section h2 {
  font-size: 2.5rem; 
  margin-bottom: 1.5rem;
}

.credentials {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.credentials input {
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 0.375rem;
}

.modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: auto;
  max-width: 80%;
  
  padding: 10px;

  border: 2px solid #ff0000;
  border-radius: 5px;
  background: #fff;

  text-align: center;
}

.modal-content {
  position: relative;
}

.close {
  position: absolute;
  top: -70%; 
  right: -2.5%;
}

button {
  cursor: pointer;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  background-color: #007BFF;
  color: white;
  font-size: 1rem;
  margin: 0.5rem;
}

button:hover {
  background-color: #0056b3;
}


.home-header {
  background-color: #007BFF;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem;
  text-align: center;
}

.home-header h1 {
  font-size: 2rem;
  font-weight: bold;
}


</style>