<template>
  <main>
    <router-link to="/login" aria-label="Log In" id="userLink">
      <button>Log In</button>
    </router-link>
    <h2 id="search">Search for a song:</h2>
    <p>{{ message2 }}</p>
    <div >
      <input v-on:keyup.enter="generalSearch" type="text" v-model="searchGeneral" placeholder="Enter Song" />
      <button @click="generalSearch">Search</button>
      <div class="songcontainerHome">
        <div class = "songHome" v-for="item in scores" :key="item.title">
            <img :src="item.song_art_image_thumbnail_url" :alt="item.title">
            <ul>
              <p>{{ item.title }}</p>
              <p>{{ item.artist }}</p>
              <button @click="playSong(item,item.title,item.artist,false)">Play Song</button>
              <p>{{ message5 }}</p>
            </ul>
            
        </div>
    </div>
    </div>
    <div id="recs" v-if="showRecs">
      <h3>Want to be recommended some songs? Select a genre:</h3> 
      <p>{{ message3 }}</p>
      <div class = "genreButtons">
      <div v-for="[key,value] in Object.entries(genres)" :key="key">
        <button class="genre" @click="recommended(key, value)">{{ value }}</button>
      </div>
    </div>
  </div>

    <div class="songcontainerHome">
      <div class = "songHome" v-for="item in recommendation" :key="item.title">
          <ul>
            <p>{{ item.title }}</p>
            <p>{{ item.artist }}</p>
            <button @click="playSong(item,item.title,item.artist,true)">Play Song</button>
            <p>{{ message5 }}</p>
          </ul>
      </div>
    </div>
    <p>Just starting?</p>

    <button @click="toggleHowTo">How to play</button>

    <HowToView v-if="howTo"/>
  </main>
</template>

<script>
import axios from 'axios';
import store from '../store';
import HowToView from './HowToView.vue';

export default {
  components: { HowToView },
  name: "HomeView",
  data() {
    return {
      searchTitle: "",
      searchArtist: "",
      searchGeneral: "",
      lyrics: "",
      message: "",
      message2: "",
      // list of songs returned from the search
      scores: [],
      genres: {
        "rap": "Rap",
        "pop": "Pop",
        "r-b": "R & B",
        "rock": "Rock",
        "country": "Country",
        "non-music": "Non-Music"
      },
      message3: "",
      // list of recommended songs based on the genre
      recommendation: [], 
      message5: "",
      showRecs: true,
      howTo: false,
    };
  },
  methods: {
    toggleHowTo() {
      this.howTo = !this.howTo;
    },
    // function to search for a song by title and artist; more specific and requires accurate input 
    // no longer used
    submitSearch() {
      const title = this.searchTitle.trim();
      const artist = this.searchArtist.trim();
      this.message = `Searching for "${title}" by "${artist}"...`;
      

      if (title && artist) {
        axios.get(`http://localhost:5001/lyrics/${encodeURIComponent(title)}/${encodeURIComponent(artist)}`)
          .then(response => {
            this.message = '';
            if (response.data.lyrics === "Lyrics not found") {
              this.message = "Lyrics not found";
            } else {
              this.message = `Found lyrics for "${title}" by "${artist}"`;
              store.commit('setLyrics', response.data.lyrics);
              store.commit('setTitle', title);
              store.commit('setArtist', artist);
              this.$router.push({
                path: '/game'
              });
            }
          })
          .catch(error => {
            this.message = `Error searching for "${title}" by "${artist}"...`;
            console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Please enter both song title and artist.");
      }
    },
    // function to search for a song by title
    generalSearch() {
      // song name
      const title = this.searchGeneral.trim();
      
      this.message3 = '';
      this.message5 = '';

      if (title) {
        this.message2 = `Searching for "${title}"...`;
        axios.get(`http://localhost:5001/genius/search/${encodeURIComponent(title)}`)
          .then(response => {
            this.scores = response.data;
            this.message2 = '';
          })
          .catch(error => {
            this.message2 = `Error searching for "${title}"...`;
            console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Please enter a song title.");
      }
    }, 
    // function to play the song/start game; passes the song title and artist to the game
    playSong(item,title, artist,recommendBool) {
      this.showRecs = false;
      this.message2 = '';
      this.message5 = `Starting game: "${title}" by "${artist}"...`;
      if (recommendBool === true) {
        this.recommendation = [item];
        this.scores = [];
      } else {
        this.recommendation = [];
        this.scores = [item];
      }

      if (title && artist) {
        axios.get(`http://localhost:5001/lyrics/${encodeURIComponent(title)}/${encodeURIComponent(artist)}`)
          .then(response => {
            this.message2 = '';
            store.commit('setLyrics', response.data.lyrics);
            store.commit('setTitle', title);
            store.commit('setArtist', artist);
            store.commit('setCover', response.data.cover);
            this.$router.push({
              path: '/game'
            });
          })
          .catch(error => {
            this.message5 = `Error starting game for "${title}" by "${artist}"...`;
            console.error("Error fetching lyrics:", error);
          });
      } else {
        alert("Something went wrong. Please try again.");
      }
    },
    // returns a list of recommended songs based on the genre
    recommended(genre, label) { 
      this.message2 = '';
      this.message5 = '';
      this.message3 = `Looking for some songs in "${label}"...`;
      axios.get(`http://localhost:5001/genius/genre/${encodeURIComponent(genre)}`)
          .then(response => {
            this.message3 = '';
            this.recommendation = response.data;
          })
          .catch(error => {
            this.message3 = `Error searching for "${genre}"...`;
            console.error("Error fetching lyrics:", error);
          });
    },
    created() {
      this.submitSearch();
      this.generalSearch();
      this.playSong();
      this.recommended();
    }
  },
};
</script>

<style>
  .genreButtons {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 20px;
  }

 .songcontainerHome {
  display: flex;
  flex-direction: column;
  align-content: flex-start;
  }

  ul {
    list-style-type: none;
  }

  img {
    width: 150px;
    border-radius: 4px;
    float: left;
    margin-right: 8px;
  }

  .songHome {
    display: flex;
    flex-direction: row;
    margin: 4px;
  }

  li:first-child {
    color:black;
    font-weight: bold;
  }

  p{
    color: black;
    font-family: titleFont;
  }

  #userLink {
    float: right;
  }
</style>
