<!-- File for the user's game statistics -->

<template>
    <div class="user">
      <h1>Game stats:</h1>

      <div class="songcontainer">
        <div class="song" v-for="item in scores" :key="item.title">
          <img :src="item.img_path" :alt="item.title">
           <ul id="stats-songlist">
            <li>{{ item.title }}</li>
            <li>{{ item.artist }}</li>
            <li>{{ item.score }}</li>
           </ul>
        </div>
      </div>
    </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        scores: [],
      }
    },
    methods: {
      getSongs() {
        const id = this.$store.state.userid;
        if(id >= 0) {
          const payload = {
            userid: 1
          }
          const path = 'http://localhost:5001/songs';
          axios.post(path, payload)
          .then((res) => {
            if(res.data.status === 'failure') {
              console.log(res.data.message);
            } else {
              this.scores = res.data.songs;
            }
          })
          .catch((error) => {
            console.error(error);
          });
        }
      },
    },
    created() {
      this.getSongs();
    },
  };
</script>

<style>
  .songcontainer {
    display:flex;
    flex-flow: row wrap;
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

  .song {
    display: block;
    width: 3.5in;
    margin: 4px;
  }
  #stats-songlist {
    background-color: #D0F5E8;
  }
</style>