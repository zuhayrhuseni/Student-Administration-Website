<template>
  <div class="not-authorized-container">
    <h2>Access Denied</h2>
    <p>You are not authorized to view this page.</p>
    <router-link to="/">Go to Home</router-link>
  </div>
</template>

<script>
//page to be displayed when a user tries to access something they are not authorized to
//can happen when a user tries to access a page that is not in their role, or when a user tries to access a page that requires them to be logged in
export default {
  name: 'NotAuthorized',
};
</script>

<style scoped>
.not-authorized-container {
  text-align: center;
  margin-top: 50px;
}

h2 {
  color: #ff0000;
}

p {
  margin-top: 10px;
}

router-link {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

router-link:hover {
  background-color: #0056b3;
}
</style>
