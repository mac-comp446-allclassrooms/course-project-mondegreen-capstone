<template>
  <main>
    <h2 id = "search"> Available Songs: </h2>
    <p>{{ message2 }}</p>
    <button @click="loadSongs">Load Songs</button>
    <div class = "songcontainerHome">
      <div class = "songHome" v-for="item in scores" :key="item">
      <ul>
        <p>{{ item }}</p>
        <button @click="playSong(item)">Play Song</button>
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
      message2: '',
      message5: '',
      scores: [],
      howTo: false
    };
  },
  methods: {
    toggleHowTo() {
      console.log('Toggle!');
      this.howTo = !this.howTo;
    },
    loadSongs() {
      console.log('Loading songs');
      axios.get(`http://localhost:5001/lyrics/list`)
        .then(response => {
        console.log(response.data.list);
        this.message2 = '';
        this.scores = response.data.list;
        for (let i = 0; i < response.data.list.length; i++) {
          setInfo(response.data.list[i]);
        }
      })
      .catch(error => {
      this.message2 = 'Failed to fetch songs';
      })
    },
    setInfo(item){
      const index = item.indexOf(':');
      const strSplit = item.split(':');
      store.setTitle(strSplit[0]);
      store.setArtist(strSplit[1]);
      store.setLyrics(strSplit[2]);
      store.setCover(strSplit[3]);
    },
    playSong(item) {
      this.message2 = '';
      this.message5 = `Starting game: "${item}"`;

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
