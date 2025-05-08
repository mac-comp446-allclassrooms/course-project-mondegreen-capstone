<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <div id="wrapper">
      <h1 id="gameTitle"><em>Those</em> are the lyrics?</h1>

      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
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
    margin-top: 5vh;
  }
</style>