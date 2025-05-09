<!-- File that contains the game page -->

<template>
  <div class="game">
    <div class="game_base">
      <div id="cover" class="item1">
        <img :src="cover" alt="Album Cover" />
      </div>
      <h2 class="item2">{{title}} by {{artist}}</h2>
      <p id="currScore" class="item3">Current Score: 0</p>
      <p id="currTotalLyrics" class="item4">Guessed Lyrics: 0/</p>
      <form class="item5">
        <label name="guess" id="guessLabel" class="item6">Enter Lyric: </label>
        <input type="text" name="guess" id="guessInput" class="item7">
        <p id="already_guessed" style="visibility:hidden;" class="item8">Already Guessed</p>
        <p id="not_lyrics" style="visibility:hidden;" class="item8">Not in Lyrics</p>
      </form>
      <button type="button" id="hintButton" class="item9">Hint</button>
      <button type="button" id="quitButton" class="item10">Give up</button>
      
    </div>
    <div id="lyrics" class="item11">
        <div></div>
      </div>
    <div class="popup">
      <div id="win_game" style="display:none;">
        <h2>Congrats! You did it!</h2>
        <p class="scoreLabel">Your Score:</p>
        <p id="score_p"></p>
        <div>
          <button type="button" id="homeButton">Try Another Song</button>
          <button type="button" id="shareButton" @click="copyToClipboardWin(title,artist)">Share Results</button>
        </div>
      </div>
      <div id="quit_game" style="display:none;">
        <h2>;-; Try again next time!</h2>
        <p class="scoreLabel">Your Score:</p>
        <p id="score_pQ"></p>
        <div>
          <button type="button" id="homeButtonQ">Try Another Song</button>
          <button type="button" id="shareButtonQ" @click="copyToClipboardQuit(title,artist)">Share Results</button>
        </div>
      </div>
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
const cover = computed(() => store.getters.getCover);
const id = computed(() => store.getters.getId);


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
    playRound(lyrics_array, title, artist, id);
    document.getElementbyId("array");
    let arrayDiv = document.createElement('div');
    arrayDiv.textContent = lyrics_array;
    document.appendChild(arrayDiv);
  }
});
// function to copy the results to clipboard; https://m-t-a.medium.com/javascript-creating-a-copy-button-with-the-clipboard-api-41bab347e601
function copyToClipboardQuit(title, artist) {
  const textToCopy = document.querySelector("#score_pQ");
  if (textToCopy) {
    navigator.clipboard.writeText("Those are the Lyrics? \n" + title + " by " + artist + "\nTry again next time ;-; \nYour score: " + textToCopy.textContent || "").then(() => {
      alert("Results copied to clipboard!");
    });
  }
}
function copyToClipboardWin(title, artist) {
  const textToCopy = document.querySelector("#score_p");
  if (textToCopy) {
    navigator.clipboard.writeText("Those are the Lyrics? \n" + title + " by " + artist + "\nCongrats! You did it! \nYour score: " + textToCopy.textContent || "").then(() => {
      alert("Results copied to clipboard!");
    });
  }
}
</script>