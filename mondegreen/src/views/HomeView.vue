<template>
  <main>
    <h1>Those are the lyrics?</h1>
    <p>Search for a song</p>
    <div>
      <input type="text" v-model="searchTitle" placeholder="Enter song" />
      <input type="text" v-model="searchArtist" placeholder="Enter artist" />
      <button @click="submitSearch">Search</button>
      {{ message }}
    </div>
    <p>Just starting?</p>
    <router-link to="/howto">
      <button>How to play</button>
    </router-link>
  </main>
</template>

<script>
import axios from 'axios';
import { nextTick } from "vue";
import store from '../store';
export default {
  name: "HomeView",
  data() {
    return {
      searchTitle: "",
      searchArtist: "",
      lyrics: "",
      message: "",
    };
  },
  methods: {
    submitSearch() {
       // song name and artist
      const title = this.searchTitle.trim();
      const artist = this.searchArtist.trim();
      this.message = `Searching for "${title}" by "${artist}"...`;

      if (title && artist) {
        axios.get(`http://localhost:5001/lyrics/${encodeURIComponent(title)}/${encodeURIComponent(artist)}`)
          .then(response => {
            this.message = '';
            store.commit('setLyrics', response.data.lyrics);
            store.commit('setTitle', title);
            store.commit('setArtist', artist);
            this.$router.push({
            path: '/game'
          });
          })
          .catch(error => {
            this.message = `Error searching for "${title}" by "${artist}"...`;
            console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Please enter both song title and artist.");
      }
    },
    created() {
      this.submitSearch();
    }
  },
};


</script>
