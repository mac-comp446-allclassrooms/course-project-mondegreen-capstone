/*
 * File for code to store lyrics, title, and artist of the songs that a user (userid) plays.
 */

import { createStore } from 'vuex';

const store = createStore({
  state: {
    lyrics: '',
    title: '',
    artist: '',
  },
  // stores values that have been "committed" to the store
  mutations: { 
    setLyrics(state, lyrics) {
      state.lyrics = lyrics;
    },
    setTitle(state, title) {
      state.title = title;
    },
    setArtist(state, artist) {
      state.artist = artist;
    },
    setCover(state, cover) {
      state.cover = cover;
    }
  },
  // retrieves values from the store
  getters: {
    getLyrics(state) {
      return state.lyrics;
    },
    getTitle(state) {
      return state.title;
    },
    getArtist(state) {
      return state.artist;
    },
    getCover(state) {
      return state.cover;
    }
  },
});

export default store;