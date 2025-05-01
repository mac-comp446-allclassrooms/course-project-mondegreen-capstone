/*
 * Functions to make the game playable.
 */

import word_freq_dict from './word_freqs.js'

import test_song from './test_song.js'
import router from './router/index.js';

class CurrentGame {
    constructor(song, currScore, word, currGuessedWordsTotal) {
        this.song = song;
        this.currScore = currScore;
        this.word = word;
        this.currGuessedWordsTotal = currGuessedWordsTotal;
    }
}

export function playRound(song) {
    console.log("playRound called");
    let game = new CurrentGame(song, 0, "", 0);
    const lyricsDiv = document.getElementById('lyrics');
    lyricsDiv.innerHTML = "";
    let scoreDiv = document.getElementById('currScore');
    let totalWords = document.getElementById('currTotalLyrics')
    totalWords.textContent = "Guessed Lyrics: 0/" + game.song.length
    let lyricDivs = [];
    for (let i = 0; i < song.length; i++) {
        let newWordDiv = document.createElement('div');
        newWordDiv.className = "one_word"
        newWordDiv.textContent = " ";
        lyricDivs.push(newWordDiv);
        lyricsDiv.appendChild(newWordDiv);
    }
    let guessButton = document.getElementById("guessButton");
    let guess = document.getElementById('guessInput');
    guessButton.addEventListener('click', function click() {
        guess = document.getElementById('guessInput');
        game.word = guess.value;
        game.currScore += checkGuessedWord(game.song, game.word, lyricDivs, game);
        scoreDiv.textContent = "Current Score: " + game.currScore;
        guess.value = "";
        totalWords.textContent = "Guessed Lyrics: " + game.currGuessedWordsTotal + "/" + song.length
        checkWin(game)
    })
    guess = document.getElementById('guessInput');
    guess.addEventListener('keypress', function(event) { // used https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
        if (event.key === "Enter") {
            event.preventDefault();
            guessButton.click();
        }
    })
}

function checkGuessedWord(song, word, lyricDivs, game) {
    let correctGuess = song.includes(word);
    if (correctGuess) {
        const currIndexes = getAllIndexes(song, word);
        for (let i = 0; i < currIndexes.length; i++) {
            const index = currIndexes[i];
            lyricDivs[index].textContent = word;
        }
        return getScore(song, word, game);
    } else if (!correctGuess) {
        return 0;
    }
}

function getScore(song, word, game) {
    // calculate how common word is in song
    let songOccurances = 0;
    song.forEach(element => (element === word && songOccurances++ && game.currGuessedWordsTotal++)); // used https://stackoverflow.com/questions/37365512/count-the-number-of-times-a-same-value-appears-in-a-javascript-array
    game.currGuessedWordsTotal++;
    let songRatio = songOccurances/song.length;
    // calculate how common word is in English
    let engOccurances = 0;
    if (word in word_freq_dict) {
        engOccurances = word_freq_dict[word];
    }
    // then determine score
    let score = calculateScore(songRatio, engOccurances);
    return score;
}

function calculateScore(songRatio, engOccurances) {
    let score = 0;
    if (songRatio >= 0.05) {
        score = 1;
    } else if (songRatio >= 0.025) {
        score = 2;
    } else if (songRatio >= 0.01) {
        score = 3;
    } else if (songRatio >= 0.005) {
        score = 4;
    } else {
        score = 5;
    }
    if (engOccurances === 0) {
        score += 5;
    } else if (engOccurances < 999999) {
        score += 4;
    } else if (engOccurances < 2605617) {//top 15000 words
        score += 3;
    } else if (engOccurances < 17864371) { //top 4000 words
        score += 2;
    } else if (engOccurances < 80755612) { //top 1000 words
        score += 1;
    }
    
    return score;
}

function checkWin(game) {
    if (game.currGuessedWordsTotal === game.song.length) {
        const winDiv = document.getElementById('win_game');
        winDiv.style.display = "block";
        const scoreP = document.getElementById('score_p');
        scoreP.textContent = game.currScore;
        const homeButton = document.getElementById('homeButton');
        homeButton.addEventListener('click', ()=> {
            router.push('/');
        });
        // const replayButton = document.getElementById('replayButton');
        // replayButton.addEventListener('click', ()=> {
        //     router.push('/game');
        //     winDiv.style.display = "none";
        // });
    }
}

// from https://stackoverflow.com/questions/20798477/how-to-find-the-indexes-of-all-occurrences-of-an-element-in-array
function getAllIndexes(song, word) {
    var indexes = [], i;
    for(i = 0; i < song.length; i++)
        if (song[i] === word)
            indexes.push(i);
    return indexes;
}

