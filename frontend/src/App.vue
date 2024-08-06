<template>
  <div id="app-wrapper">
    <AppHeader title="Section 1 Group 7 Course System" />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import AppHeader from "./components/AppHeader.vue";
</script>
