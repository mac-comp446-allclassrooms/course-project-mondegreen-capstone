/*
 * Functions to make the game playable.
 */

import word_freq_dict from './word_freqs.js'

class CurrentGame {
    constructor(song, currScore, word, currGuessedWordsTotal) {
        this.song = song;
        this.currScore = currScore;
        this.word = word;
        this.currGuessedWordsTotal = currGuessedWordsTotal;
    }
}

function playRound() {
    
}


function checkGuessedWord(song, word) {
    correctGuess = song.includes(word);
    if (correctGuess) {
        currGuessedWordsTotal += 1;
        calculateScore(song, word);
    } else if (!correctGuess) {
        word = "";
    }
}

function getScore(song, word) {
    // calculate how common word is in song
    let songOccurances = 0;
    song.forEach(element => (element === word && songOccurances++)); // used https://stackoverflow.com/questions/37365512/count-the-number-of-times-a-same-value-appears-in-a-javascript-array
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
        score = 5;
    } else if (songRatio >= 0.025) {
        score = 4;
    } else if (songRatio >= 0.01) {
        score = 3;
    } else if (songRatio >= 0.005) {
        score = 2;
    } else {
        score = 1;
    }
    if (engOccurances >= 80755612) { //top 1000 words
        score += 1;
    } else if (engOccurances >= 17864371) { //top 4000 words
        score += 2;
    } else if (engOccurances >= 2605617) {//top 15000 words
        score += 3;
    }
}

