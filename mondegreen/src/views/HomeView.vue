<template>
  <main>
    <h2 id = "search"> Available Songs: </h2>
    <p>{{ message2 }}</p>
    <div class = "songcontainerHome">
      <div class = "songHome" v-for="item in scores" :key="item">
      <ul>
        <p> {{ getTitle(item) }}</p>
        <p> {{ getArtist(item) }}</p>
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
  created() {
    console.log('Loading songs');
      axios.get(`https://those-are-the-lyrics-fe11728950ff.herokuapp.com/lyrics/list`)
        .then(response => {
          this.scores = response.data.list;
      })
      .catch(error => {
      this.message2 = 'Failed to fetch songs';
      })
  },
  methods: {
    toggleHowTo() {
      console.log('Toggle!');
      this.howTo = !this.howTo;
    },
    getTitle(item){
      const strSplit = item.split(':');
      const title = strSplit[0];
      const clean_title = title.replaceAll("-", " ");
      return clean_title;
    },
    getArtist(item){
      const strSplit = item.split(':');
      const artist = strSplit[1];
      const clean_artist = artist.replaceAll("-", " ");
      return clean_artist;
    },
    playSong(item) {
      this.message2 = '';
      this.message5 = `Starting game: "${item}"`;
      const strSplit = item.split(':');
      const raw_title = strSplit[0];
      const title = raw_title.replaceAll("-", " ");
      const raw_artist = strSplit[1];
      const artist = raw_artist.replaceAll("-", " ");
      const url = `https://those-are-the-lyrics-fe11728950ff.herokuapp.com/lyrics/${encodeURIComponent(raw_title.toLowerCase())}/${encodeURIComponent(raw_artist.toLowerCase())}` 
      console.log(url)
      axios.get(url)
        .then(response => {
          
          const lyrics = response.data.lyrics;
          store.commit('setLyrics', lyrics);
          store.commit('setTitle', raw_title);
          store.commit('setArtist', raw_artist);
          this.$router.push({
            path: '/game'
          });
        })
      .catch(error => {
      this.message2 = 'Failed to fetch lyrics';
      })  
    }
  }
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
