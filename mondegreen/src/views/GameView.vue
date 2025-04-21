<template>
  <div class="game">
    <h1>Play Game</h1>
    <h2>Firework by Katy Perry</h2>
    <p>
        <p id="currScore">
          Current Score: 0
        </p>
        <p id="currTotalLyrics">
            &#9; Guessed Lyrics: 0/
        </p>
      </p>
    <form>
        <label name="guess">Enter Lyric</label>
        <input type="text" name="guess" id="guessInput">
        <p>
            <button type="button" id="guessButton">Guess</button>
        </p>
    </form>
    <button type="button" id="hintButton">Hint</button>
    <div id="lyrics">

    </div>
  </div>
  <div id="win_game" style="display:none">
    <h2>Congrats! You did it!</h2>
    <p>Your Score:</p>
    <p id="score_p"></p>
    <div>
      <button type="button" id="homeButton">Try Another Song</button>
      <button type="button" id="replayButton">Replay</button>
      <button type="button" id="shareButton">Share Results</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { playRound } from '../game_logic.js'

onMounted(() => {
  playRound()
})
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