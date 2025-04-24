<template>
  <main>
    <h1>Those are the lyrics?</h1>
    <p>Search for a song</p>
    <div>
      <input type="text" v-model="searchTitle" placeholder="Enter song" />
      <input type="text" v-model="searchArtist" placeholder="Enter artist" />
      <button @click="submitSearch">Search</button>
    </div>
    {{ lyrics }}
    <p>Just starting?</p>
    <router-link to="/howto">
      <button>How to play</button>
    </router-link>
  </main>
</template>

<script>
import axios from 'axios';
export default {
  name: "HomeView",
  data() {
    return {
      searchTitle: "",
      searchArtist: "",
      lyrics: "",
    };
  },
  methods: {
    submitSearch() {
       // song name and artist
      const title = this.searchTitle.trim();
      const artist = this.searchArtist.trim();

      if (title && artist) {
        axios.get(`http://localhost:5001/lyrics/${encodeURIComponent(title)}/${encodeURIComponent(artist)}`)
          .then(response => {
            this.lyrics = response.data.lyrics;
          })
          .catch(error => {
        console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Please enter both song title and artist.");
      }
    },
    created() {
      this.submitSearch();
    },
  },
};


</script>
