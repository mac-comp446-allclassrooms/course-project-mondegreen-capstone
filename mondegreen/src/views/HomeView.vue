<template>
  <main>
    <h1>Those are the lyrics?</h1>
    <p>Search for a song</p>
    <div>
      <input type="text" v-model="searchTitle" placeholder="Enter song" />
      <input v-on:keyup.enter="submitSearch" type="text" v-model="searchArtist" placeholder="Enter artist" />
      <button @click="submitSearch">Search</button>
      {{ message }}
    </div>
    <p>Or</p>
    <p>More general search</p>
    <div>
      <input v-on:keyup.enter="generalSearch" type="text" v-model="searchGeneral" placeholder="Enter Song" />
      <button @click="generalSearch">Search</button>
      <div class="song" v-for="item in scores" :key="item.title">
          <img :src="item.song_art_image_thumbnail_url" :alt="item.title">
           <ul>
            <li>{{ item.title }}</li>
            <li>{{ item.artist }}</li>
           </ul>
      </div>
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
      message2: "",
      scores: [],
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
    generalSearch() {
      // song name
      const title = this.searchGeneral.trim();
      this.message2 = `Searching for "${title}"...`;

      if (title) {
        axios.get(`http://localhost:5001/genius/search2/${encodeURIComponent(title)}`)
          .then(response => {
            this.message2 = response.data;
            this.scores = response.data;
          })
          .catch(error => {
            this.message2 = `Error searching for "${title}"...`;
            console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Please enter a song title.");
      }
    },    
    created() {
      this.submitSearch();
      this.generalSearch();
    }
  },
};


</script>
