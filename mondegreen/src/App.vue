<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="wrapper">
    <h1>Site Title</h1>

    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/user">View Profile</RouterLink>
    </nav>

  </div>

  <div class="content">
    <RouterView/>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
  .content {
    display: flex;
    justify-content: center;
    align-items: center;
    /* height:75vh; */
    margin-top: 5vh;
  }
</style>