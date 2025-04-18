<template>
  <main>
    <h1>Those are the lyrics?</h1>
    <p>Search for a song</p>
    <div>
      <input type="text" v-model="searchQuery" placeholder="Enter song or artist" />
      <button @click="submitSearch">Search</button>
    </div>
    <p>Just starting?</p>
    <router-link to="/howto">
      <button>How to play</button>
    </router-link>
  </main>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    submitSearch() {
      alert("Searching for: "+ this.searchQuery);
    },
  },
};


</script>
