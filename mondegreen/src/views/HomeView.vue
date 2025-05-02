<template>
  <main>
    <h1>Those are the lyrics?</h1>
    <p>Search for a song</p>
    <!-- <div>
      <input type="text" v-model="searchTitle" placeholder="Enter song" />
      <input v-on:keyup.enter="submitSearch" type="text" v-model="searchArtist" placeholder="Enter artist" />
      <button @click="submitSearch">Search</button>
      {{ message }}
    </div>
    <p>Or</p> -->
    {{ message2 }}
    <!-- <p>More general search</p> -->
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
              {{ message5 }}
            </ul>
            
        </div>
    </div>
    </div>
    <h2>Want to be recommended some songs? Select a genre</h2> 
    {{ message3 }}
    <div class = "genreButtons">
    <div v-for="genre in genres" :key="genre">
      <button @click="recommended(genre)">{{ genre }}</button>
    </div>
  </div>

    <div class="songcontainerHome">
      <div class = "songHome" v-for="item in recommendation" :key="item.title">
          <img style="width: 10%; background-color: aliceblue;" src="../assets/image.png" :alt="item.title">
          <ul>
            <p>{{ item.title }}</p>
            <p>{{ item.artist }}</p>
            <button @click="playSong(item,item.title,item.artist,true)">Play Song</button>
            {{ message5 }}
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
      genres: ["rap", "pop", "r-b", "rock", "country", "non-music"],
      message3: "",
      recommendation: [],
      message5: "",
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
    generalSearch() {
      // song name
      const title = this.searchGeneral.trim();
      this.message2 = `Searching for "${title}"...`;
      this.message2 = '';
      this.message3 = '';
      this.message5 = '';

      if (title) {
        axios.get(`http://localhost:5001/genius/search2/${encodeURIComponent(title)}`)
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
    playSong(item,title, artist,recommendBool) {
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
    recommended(genre) {
      this.message2 = '';
      this.message5 = '';
      this.message3 = `Looking for some songs in "${genre}"...`;
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
  flex-wrap: wrap;
  align-content: center;
  }

  ul {
    list-style-type: none;
  }

  img {
    width: 25%;
    border-radius: 4px;
    float: left;
    margin-right: 8px;
  }

  .songHome {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 4px;
  }

  li:first-child {
    color:black;
    font-weight: bold;
  }

  p{
    color: #714EBB;
    font-family: titleFont;
  }

</style>
