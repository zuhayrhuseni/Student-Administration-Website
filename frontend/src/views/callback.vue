<template>
  <div class="loading-page">
    <p>Loading...</p>
  </div>
</template>

<script setup>
//post login page - used for redirection
import { useAuth0 } from '@auth0/auth0-vue';
import { watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';

//router, auth0
const router = useRouter();
const { user } = useAuth0();

//Auth0 information
let userID = '';
let role = null;
let Name = null;
let done = false;

//watching for auth0 update - this is necessary to get user info and track authorization
watch(user,async (newUser) => {
    if (newUser && newUser.nickname) {
        //store info and Role metadata
        userID = newUser;
        role = newUser['dev-75fp6aop37uung0c.us.auth0.com/Role'];
        Name = newUser['dev-75fp6aop37uung0c.us.auth0.com/full_name'];
        //waiting here as a bug fix - originally would have to refresh page for redirection to occur
        await nextTick();
        await new Promise(resolve => setTimeout(resolve, 0));
        //call to find user
        auth0Login();
        //adding wait for DB to update - avoids "User not found"
        while (!done) {
            await nextTick();
            await new Promise(resolve => setTimeout(resolve, 0));
        }
        //Redirect based on the user's role
        if (role == 'Teacher') {
            router.push('/teacherhome');
        } else if (role == 'Student') {
            router.push('/studenthome');
        }
        else if (role == 'Admin') {
            router.push('/adminhome');
        }
    }
}, { immediate: true });

//API call to update DB with new users
function auth0Login() {
    let endpoint = 'https://74ym2fsc17.execute-api.us-east-1.amazonaws.com/ProjAPI/auth0Login';
    fetch(endpoint, {
    method: 'POST',
    body: JSON.stringify({
        "Name": Name,
        "UserID": userID.nickname,
        "Type": role
    }),
    headers: {
        'Content-Type': 'application/json'
    },
    })
    .then(response => response.json())
    .then(data => {
    if (data.statusCode === 200) {
        //sucess
        console.log(data.body);
        done = true;
    }
    else {
        window.alert(`An error occurred updating the databse`);
        done = true;
    }
    })
    .catch(error => {
    console.error('An error has occurred: ', error);
    });
};

</script>

<style>
.loading-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.5rem;
}
</style>
