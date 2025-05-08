<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <div id="wrapper">
      <h1><em>Those</em> are the lyrics?</h1>

      <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/user">User Stats</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Sign up</RouterLink>
      </nav> -->

      <router-view :key="$route.fullPath"/>
    </div>
<div>
  <!-- <router-view v-slot="{ Component }">
    <component :is="Component" />
  </router-view> -->
</div>
    

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