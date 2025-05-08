<template>
  <div>
    <router-link to="/" aria-label="<-">
      <button><-</button>
    </router-link>
    <h1>{{ loggedIn ? "Log Out" : (isLogin ? "Log In" : "Create Account") }}</h1>
    <form @submit.prevent="handleActions">
      <div v-if="!loggedIn">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="unField"/>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="pwField"/>
        <br>
        <div v-if="!isLogin">
          <label for="passwordC" class="signup">Confirm Password:</label>
          <input type="password" id="passwordC" v-model="conField"/>
        </div>
        <br>
      </div>
      <button type="submit">{{ loggedIn ? "Log Out" : (isLogin ? "Log In" : "Create Account") }}</button>
      <button @click="toggleButton">{{ isLogin ? "Go to Sign up" : "Go to Log In" }}</button>
    </form>
  </div>
  <span>{{ message }}</span>
</template>

<script>
  import axios from 'axios';
  import store from '../store';
  

  export default {
    data () {
      return {
        message: '',
        username: '',
        unField: '',
        pwField: '',
        conField: '',
        isLogin: true,
        loggedIn: false,
      }
    },
    methods: {
      login(payload) {
        const path = 'http://localhost:5001/login';
        axios.post(path, payload)
        .then((response) => {
          this.loginResponse(response);
        })
        .catch((error) => {
          console.log(error);
        });
      },
      signup(payload) {
        const path = 'http://localhost:5001/signup';
        axios.post(path, payload)
        .then(function (response) {
          this.loginResponse(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      handleActions() {
        if(this.loggedIn) {
          this.logout();
        }

        const un = this.unField.trim();
        const pw = this.pwField.trim();

        if (!this.isLogin) {
          const con = this.conField.trim();
          if (con !== pw) {
            this.message = 'Passwords must match!';
            return;
          }
        }

        if (this.verifyInput(un) && this.verifyInput(pw)) {
          const payload = {
            username: un,
            password: pw,
          }
          this.isLogin ? this.login(payload) : this.signup(payload);
          this.message = '';
          this.unField = '';
          this.pwField = '';
          this.conField = '';
        } else {
          this.message = 'Username and password must contain only alphanumeric characters!'
        }
      },
      loginResponse(response) {
        console.log(response.data, " from loginResponse");
        if (response.data.status === 'success') {
          this.message = 'logged in';
          this.loggedIn = true;
          const id = response.data.id;
          console.log("from loginResponse ", id);
          store.commit('setId', id);
          
        } else if (response.data.status === 'failure') {
          this.message = response.data.message;
        } else {
          this.message = 'unknown error!'
        }
      },
      verifyInput(str) {
        if (! /^[a-zA-Z0-9]+$/.test(str)) {
          // Validation failed
          return false;
        } else {
          return true;
        }
      },
      logout() {
        const path = 'http://localhost:5001/logout';
        axios.post(path)
        .then(function (response) {
          this.message = 'Successfully logged out!';
        })
        .catch(function (error) {
          console.log(error);
        });
        this.loggedIn = false;
      },
      toggleButton() {
        this.isLogin = !this.isLogin;
      },
    },
    created() {
    },
  };
</script>

<style>
  button {
    margin: 4px;
  }
</style>