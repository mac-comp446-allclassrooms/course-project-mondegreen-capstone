import { createStore } from 'vuex';

const store = createStore({
  state: {
    lyrics: '',
    title: '',
    artist: '',
  },
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
  },
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
  },
});

export default store;