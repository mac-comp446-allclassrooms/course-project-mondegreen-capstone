<template>
  <div class="game">
    <h1>Play Game</h1>
    <h2>{{title}} by {{artist}}</h2>
    <p id="currScore">Current Score: 0</p>
    <p id="currTotalLyrics">Guessed Lyrics: 0/</p>
    <!-- {{ lyrics }} -->
    <form>
      <label name="guess">Enter Lyric</label>
      <input type="text" name="guess" id="guessInput">
      <button type="button" id="guessButton">Guess</button>
    </form>
    <button type="button" id="hintButton">Hint</button>
    <div id="lyrics">
      <p></p>
    </div>
  </div>
  <div id="win_game" style="display:none">
    <h2>Congrats! You did it!</h2>
    <p>Your Score:</p>
    <p id="score_p"></p>
    <div>
      <button type="button" id="homeButton">Try Another Song</button>
      <button type="button" id="shareButton">Share Results</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { playRound } from '../game_logic.js';
import store from '../store';

const route = useRoute();
let lyrics = computed(() => store.getters.getLyrics);
const title = computed(() => store.getters.getTitle);
const artist = computed(() => store.getters.getArtist);

lyrics.value = lyrics.value.replace(/_/g, ' ');
const lyrics_array = lyrics.value.split(" ");
lyrics_array.shift();
console.log(lyrics_array);
console.log(lyrics.value);

onMounted(() => {
  // if (lyrics.value === "Lyrics not found") {
    // alert("Lyrics not found")
  // } else {
    playRound(lyrics_array);
  // }
});
</script>

<style scoped>
.game {
  width: 100%;
  padding: 20px;
}

#lyrics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  margin-top: 10px;
}

#win_game {
  position: absolute;
  width: 70%;
  height: 30%;
  background: hsla(160, 100%, 37%, 1);
  color: black;
  margin: auto;
  padding: 5%;
  text-align: center;
}

#score_p {
  background: white;
  color: black;
  font-size: x-large;
  text-align: center;
}

</style>