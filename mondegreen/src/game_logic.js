/*
 * Functions to make the game playable.
 */

import word_freq_dict from './word_freqs.js'

import router from './router/index.js';
import axios from 'axios';

class CurrentGame {
    constructor(song, currScore, word, currGuessedWordsTotal, title, artist, id) {
        this.song = song;
        this.currScore = currScore;
        this.word = word;
        this.currGuessedWordsTotal = currGuessedWordsTotal;
        this.title = title;
        this.artist = artist;
        this.userid = id;
    }
}

export function playRound(song, title, artist, id) {
    console.log("playRound called");
    let game = new CurrentGame(song, 0, "", 0, title, artist, id);
    const lyricsDiv = document.getElementById('lyrics');
    lyricsDiv.innerHTML = "";
    let scoreDiv = document.getElementById('currScore');
    let totalWords = document.getElementById('currTotalLyrics')
    totalWords.textContent = "Guessed Lyrics: 0/" + game.song.length
    let lyricDivs = [];
    let userGuesses = [];
    for (let i = 0; i < song.length; i++) {
        let newWordDiv = document.createElement('div');
        newWordDiv.className = "one_word"
        newWordDiv.textContent = "";
        lyricDivs.push(newWordDiv);
        lyricsDiv.appendChild(newWordDiv);
    }
    let guess = document.getElementById('guessInput');
    guess.onkeyup = function() {
        guess = document.getElementById('guessInput');
        game.word = guess.value.replace(/[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/g, '').toLowerCase(); // used https://www.geeksforgeeks.org/how-to-remove-punctuation-from-text-using-javascript/;
        if (game.song.includes(game.word)) {
            if (!userGuesses.includes(game.word)) {
                game.currScore += checkGuessedWord(game.song, game.word, lyricDivs, game);
                userGuesses.push(game.word);
                setTimeout(function() {
                    guess.value = "";
                }, 200);
            } else {
                guess.addEventListener('keypress', function(event) { // used https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
                    if (event.key === "Enter" && game.song.includes(game.word)) {
                        const temp_word = game.word;
                        event.preventDefault();
                        let already_guessed = document.getElementById("already_guessed");
                        already_guessed.style.visibility = "visible";
                        setTimeout(function() {
                            already_guessed.style.visibility = "hidden";
                            if (guess.value === temp_word) {
                                guess.value = "";
                            }
                        }, 2000);
                    }
                });
            }
            scoreDiv.textContent = "Current Score: " + game.currScore;
            // guess.value = "";
            totalWords.textContent = "Guessed Lyrics: " + game.currGuessedWordsTotal + "/" + song.length
            checkWin(game, title, artist)
        } else {
            guess.addEventListener('keypress', function(event) { // used https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
                if (event.key === "Enter" && !game.song.includes(game.word)) {
                    const temp_word = game.word;
                    event.preventDefault();
                    let not_lyrics = document.getElementById("not_lyrics");
                    not_lyrics.style.visibility = "visible";
                    setTimeout(function() {
                        not_lyrics.style.visibility = "hidden";
                        if (guess.value === temp_word) {
                            guess.value = "";
                        }
                    }, 2000);
                }
            });
        }
    }
    document.getElementById("hintButton").disabled = false;
    document.getElementById("quitButton").disabled = false;
    const hint_button = document.getElementById("hintButton");
    hint_button.addEventListener('click', ()=> {
        let randI = Math.floor(Math.random() * game.song.length); // used https://www.geeksforgeeks.org/how-to-select-a-random-element-from-array-in-javascript/
        let randLyric = game.song[randI];
        while (userGuesses.includes(randLyric)) {
            randI = Math.floor(Math.random() * game.song.length);
            randLyric = game.song[randI];
        }
        userGuesses.push(randLyric);
        checkHintWord(song, randLyric, lyricDivs, game, title, artist);
        totalWords.textContent = "Guessed Lyrics: " + game.currGuessedWordsTotal + "/" + song.length
    });
    const quit_button = document.getElementById("quitButton");
    quit_button.addEventListener('click', ()=> {
        document.getElementById("hintButton").disabled = true;
        document.getElementById("quitButton").disabled = true;
        const quitDiv = document.getElementById('quit_game');
        quitDiv.style.display = "block";
        const scoreP = document.getElementById('score_pQ');
        scoreP.textContent = game.currScore;
        const homeButton = document.getElementById('homeButtonQ');

        pushScore(title, artist, game.currScore, userid);

        homeButton.addEventListener('click', ()=> {
            router.push('/');
            setTimeout(() => {
                window.location.reload();
            }, 500);
        });
    });
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

function checkHintWord(song, word, lyricDivs, game, title, artist) {
    const currIndexes = getAllIndexes(song, word);
    for (let i = 0; i < currIndexes.length; i++) {
        const index = currIndexes[i];
        lyricDivs[index].textContent = word;
        lyricDivs[index].style.backgroundColor = '#EDB9DD';
        lyricDivs[index].style.color = '#0E60AD';
    }
    game.currGuessedWordsTotal += currIndexes.length;
    checkWin(game, title, artist);
}

function getScore(song, word, game) {
    // calculate how common word is in song
    let songOccurances = 0;
    song.forEach(element => (element === word && songOccurances++)); // used https://stackoverflow.com/questions/37365512/count-the-number-of-times-a-same-value-appears-in-a-javascript-array
    game.currGuessedWordsTotal += songOccurances;
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
    } else if (engOccurances < 2605617) { //top 15000 words
        score += 3;
    } else if (engOccurances < 17864371) { //top 4000 words
        score += 2;
    } else if (engOccurances < 80755612) { //top 1000 words
        score += 1;
    }
    
    return score;
}

function checkWin(game, title, artist) {
    if (game.currGuessedWordsTotal === game.song.length) {
        document.getElementById("hintButton").disabled = true;
        document.getElementById("quitButton").disabled = true;
        const winDiv = document.getElementById('win_game');
        winDiv.style.display = "block";
        const scoreP = document.getElementById('score_p');
        scoreP.textContent = game.currScore;

        pushScore(title, artist, game.currScore, userid);

        const homeButton = document.getElementById('homeButton');
        homeButton.addEventListener('click', ()=> {
            router.push('/');
        });
    }
}

function unwrap(val) {
    if (val.value !== null) {
        return val.value;
    } else {
        return val;
    }
}

function pushScore(title, artist, score, id) {
    if(id < 0) {
        return false;
    }
    const payload = {
        userid: id,
        title: unwrap(title),
        artist: unwrap(artist),
        score: unwrap(score),
    };

    const path = 'http://localhost:5001/addsong';
        axios.post(path, payload)
        .then((response) => {
          return response.data.status === 'success';
        })
        .catch((error) => {
          console.log(error);
          return false;
        });
}

// from https://stackoverflow.com/questions/20798477/how-to-find-the-indexes-of-all-occurrences-of-an-element-in-array
function getAllIndexes(song, word) {
    var indexes = [], i;
    for(i = 0; i < song.length; i++)
        if (song[i] === word)
            indexes.push(i);
    return indexes;
}

