/*
 * Functions to make the game playable.
 */

class CurrentGame {
    constructor(song, currScore, word, currGuessedWordsTotal) {
        this.song = song;
        this.currScore = currScore;
        this.word = word;
        this.currGuessedWordsTotal = currGuessedWordsTotal;
    }
}


function guessedWord(song, word) {
    correctGuess = song.includes(word);
    if (correctGuess) {
        currGuessedWordsTotal += 1;
        calculateScore(song, word);
    } else if (!correctGuess) {
        word = "";
    }
}

function calculateScore(song, word) {
    // calculate how common word is in song
    let occurances = 0;
    song.forEach(element => (element === word && occurances++)); // used https://stackoverflow.com/questions/37365512/count-the-number-of-times-a-same-value-appears-in-a-javascript-array
    // calculate how common word is in English
    
    // then determine score
}

