// this file creates the router instance that is used by our application

// we start by importing the createRouter and createWebHistory functions, as well as the components describing each of our views
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import StudentHomeView from "../views/Student/StudentHomeView.vue"
import StudentCourseSearchView from "../views/Student/CourseSearchStudentView.vue" 
import TeacherView from "../views/Teacher/TeacherView.vue"


const router = createRouter({
  // the history mode determines how vue router interacts with the url.
  // createWebHistory() simulates the default browser behavior of changing
  // the path of the url based on the current document.
  // import.meta.env.BASE_URL is a vite feature that you don't need to worry about
  // and can safely use. it refers to the current path to the directory being
  // served by vite, which in this project is always the same directory
  // (and therefore import.meta.env.BASE_URL is '/')
  history: createWebHistory(import.meta.env.BASE_URL),

  // each entry to this routes array has a path (what goes in the URL to access
  // this page), a name (check out components/AppHeader.vue for how this is used)
  // and, most importantly, the component that should be rendered for the view
  routes: [
    {
      path: "/home",
      name: "home",
      component: HomeView,
    },
    {
      path: "/studenthome",
      name: "studenthome",
      component: StudentHomeView,
    },
    {
      path: "/studentcs/:user",
      name: "studentcs",
      component: StudentCourseSearchView,
      props: true,
    },
    {
      path: "/teacherhome",
      name: "teacherhome",
      component: TeacherView
    },
    {
      path: '/:pathMatch(.*)*', // This will catch all routes that don't match the above ones
      redirect: '/home',
    },
  ],
});

export default router;
