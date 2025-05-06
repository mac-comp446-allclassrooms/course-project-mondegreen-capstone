<template>
  <div class="game">
    <div id="cover">
      <img :src="cover" alt="Album Cover" />
    </div>
    <h2>{{title}} by {{artist}}</h2>
    <p id="currScore">Current Score: 0</p>
    <p id="currTotalLyrics">Guessed Lyrics: 0/</p>
    <div id="win_game" style="display:none;">
    <h2>Congrats! You did it!</h2>
    <p>Your Score:</p>
    <p id="score_p"></p>
    <div>
      <button type="button" id="homeButton">Try Another Song</button>
      <button type="button" id="shareButton" @click="copyToClipboardWin">Share Results</button>
    </div>
  </div>
  <div id="quit_game" style="display:none;">
    <h2>;-; Try again next time!</h2>
    <p>Your Score:</p>
    <p id="score_pQ"></p>
    <div>
      <button type="button" id="homeButtonQ">Try Another Song</button>
      <button type="button" id="shareButtonQ" @click="copyToClipboardQuit">Share Results</button>
    </div>
  </div>
    <form>
      <label name="guess" id="guessLabel">Enter Lyric: </label>
      <input type="text" name="guess" id="guessInput">
      <p id="already_guessed" style="display:none;">Already Guessed</p>
      <p id="not_lyrics" style="display:none;">Not in Lyrics</p>
    </form>
    <button type="button" id="hintButton">Hint</button>
    <button type="button" id="quitButton">Give up</button>
    <div id="lyrics">
      <div></div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
// import func from '../../../vue-temp/vue-editor-bridge.js';
import { playRound } from '../game_logic.js';
import store from '../store';

const route = useRoute();
let lyrics = computed(() => store.getters.getLyrics);
const title = computed(() => store.getters.getTitle);
const artist = computed(() => store.getters.getArtist);
const cover = computed(() => store.getters.getCover);


lyrics.value = lyrics.value.replace(/_/g, ' ');
const lyrics_array = lyrics.value.split(" ");
lyrics_array.shift();
lyrics_array.id = "array"
console.log(lyrics_array);
console.log(lyrics.value);

onMounted(() => {
  if (lyrics.value === "Lyrics not found") {
    alert("Lyrics not found")
  } else {
    playRound(lyrics_array);
    document.getElementbyId("array");
    let arrayDiv = document.createElement('div');
    arrayDiv.textContent = lyrics_array;
    document.appendChild(arrayDiv);
  }
});
function copyToClipboardQuit() {
  const textToCopy = document.querySelector("#score_pQ");
  if (textToCopy) {
    navigator.clipboard.writeText("Try again next time ;-; \n Your score: " + textToCopy.textContent || "").then(() => {
      alert("Results copied to clipboard!");
    });
  }
}
function copyToClipboardWin() {
  const textToCopy = document.querySelector("#score_p");
  if (textToCopy) {
    navigator.clipboard.writeText("Congrats! You did it! \n Your score: " + textToCopy.textContent || "").then(() => {
      alert("Results copied to clipboard!");
    });
  }
}
</script>