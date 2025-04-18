/*
 * Functions to make the game playable.
 */

import word_freq_dict from './word_freqs.js'

import test_song from './test_song.js'

class CurrentGame {
    constructor(song, currScore, word, currGuessedWordsTotal) {
        this.song = song;
        this.currScore = currScore;
        this.word = word;
        this.currGuessedWordsTotal = currGuessedWordsTotal;
    }
}

export function playRound() {
    console.log("playRound called");
    let game = new CurrentGame(test_song, 0, "", 0);
    const lyricsDiv = document.getElementById('lyrics');
    let scoreP = document.getElementById('currScore');
    let totalWords = document.getElementById('currTotalLyrics')
    totalWords.textContent = "Guessed Lyrics: 0/" + test_song.length
    let lyricPs = [];
    for (let i = 0; i < test_song.length; i++) {
        let newWordP = document.createElement('p');
        newWordP.textContent = " ";
        lyricPs.push(newWordP);
        lyricsDiv.appendChild(newWordP);
    }
    let guessButton = document.getElementById("guessButton");
    guessButton.addEventListener('click', ()=> {
        let guess = document.getElementById('guessInput');
        game.word = guess.value;
        game.currScore += checkGuessedWord(game.song, game.word, lyricPs, game);
        scoreP.textContent = "Current Score: " + game.currScore;
        guess.value = "";
        totalWords.textContent = "Guessed Lyrics: " + game.currGuessedWordsTotal + "/" + test_song.length
    })
}


function checkGuessedWord(song, word, lyricPs, game) {
    let correctGuess = song.includes(word);
    if (correctGuess) {
        const currIndexes = getAllIndexes(song, word);
        for (let i = 0; i < currIndexes.length; i++) {
            const index = currIndexes[i];
            lyricPs[index].textContent = word;
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

// from https://stackoverflow.com/questions/20798477/how-to-find-the-indexes-of-all-occurrences-of-an-element-in-array
function getAllIndexes(song, word) {
    var indexes = [], i;
    for(i = 0; i < song.length; i++)
        if (song[i] === word)
            indexes.push(i);
    return indexes;
}

