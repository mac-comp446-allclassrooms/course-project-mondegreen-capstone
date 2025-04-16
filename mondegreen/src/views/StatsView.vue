<template>
    <div class="user">
      <h1>This is where user stats will go</h1>

      <div class="songcontainer">
        <div class="song" v-for="item in scores" :key="item.title">
          <img :src="item.img_path" :alt="item.title">
           <ul>
            <li>{{ item.title }}</li>
            <li>{{ item.artist }}</li>
            <li>{{ item.score }}</li>
           </ul>
        </div>
      </div>
    </div>
</template>

<script>
  function Score(title, artist, img_path, score) {
    this.title = title;
    this.artist = artist;
    this.img_path = img_path; // replace with api call? or store links in db
    this.score = score;
  }

  const scores = [
    new Score("symbol", "Adrianne Lenker", "https://images.genius.com/ea813421a18bde3bc39b73c110b0ab2c.300x300x1.jpg", 100),
    new Score("Cloudbusting","Kate Bush","https://images.genius.com/c3e6f6097640bca27833078355fd647e.300x300x1.png", 75),
    new Score("Simulation Swarm", "Big Thief", "https://images.genius.com/26084cc61b6b1849e2c762fd0ca709fc.300x300x1.png", 80),
    new Score("Pump Up the Jam", "Technotronic", "https://images.genius.com/a3992138b1d56a1238150be0051cb321.300x300x1.png", 25),
    new Score("Juna", "Clairo", "https://images.genius.com/6725f1000db2e875f4ce966f4144d41a.300x300x1.png", 37),
    new Score("Hello Hello Hello", "Remi Wolf", "https://images.genius.com/9d9b505e394955ec1e750059846258c6.300x300x1.png", 100),
    new Score("Linger", "The Cranberries", "https://images.genius.com/faeabffde6e1ce2c6ffafe4b5d01d4ab.300x300x1.png", 34),
    new Score("Blister In The Sun", "Violent Femmes", "https://images.genius.com/af35b7cdb9d07071e3946098f542377b.300x295x1.jpg", 99)
  ];

  export default {
    data () {
      return {
        scores
      }
    }
  }
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

  li:first-child {
    color:lightgray;
    font-weight: bold;
  }
</style>