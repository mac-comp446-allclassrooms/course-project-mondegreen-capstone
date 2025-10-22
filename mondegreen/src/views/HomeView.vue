<template>
  <main>
    <h2 id = "search"> Available Songs: </h2>
    <p>{{ message2 }}</p>
    <div class = "songcontainerHome">
      <div class = "songHome" v-for="item in scores" :key="item">
      <ul>
        <p>{{ item }}</p>
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
      scores: [],
      howTo: false
    };
  },
  methods: {
    toggleHowTo() {
      this.howTo = !this.howTo;
    },
    loadSongs() {
      axios.get(`http://localhost:5001/lyrics/list`)
        .then(response => {
        this.message2 = '';
        this.scores = response.data;
      })
      .catch(error => {
      this.message2 = 'Failed to fetch songs';
      })
    },
    created() {
      this.loadSongs()
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
