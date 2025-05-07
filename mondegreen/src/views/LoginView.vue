<template>
  <div>
    <h1>{{ isLogin ? "Log In" : "Create Account" }}</h1>
    <form @submit.prevent="handleActions">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="unField"/>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="pwField"/>
        <br>
        <div v-if="!isLogin">
          <label for="passwordC" class="signup">Confirm Password:</label>
          <input type="passwordC" id="passwordC" v-model="conField"/>
        </div>
        <br class="signup hidden">
      <button type="submit">{{ isLogin ? "Log In" : "Create Account" }}</button>
      <button @click="toggleButton">{{ isLogin ? "Go to Sign up" : "Go to Log In" }}</button>
    </form>
  </div>
  <span>{{ message }}</span>
</template>

<script>
  import axios from 'axios';

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
        const path = 'http://localhost:5001/post/malone';
        axios.post(path, payload)
        .then(function (response) {
          handleResponse(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      signup(payload) {
        const path = 'http://localhost:5001/signup';
        axios.post(path, payload)
        .then(function (response) {
          handleResponse(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      handleActions() {
        if(false) {
          this.logout();
        }

        const un = this.unField.trim();
        const pw = this.pwField.trim();

        if (!this.isLogin) {
          const con = this.conField.trim();
          if (con !== pw) {
            this.message = 'Passwords must match!';
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
      handleResponse(response) {
        if (response.data.status === 'success') {
          this.message = 'logged in';
          this.loggedIn = true;
        } else {
          this.message = response.data.message;
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
      },
      toggleButton() {
        this.isLogin = !this.isLogin;
      },
    },
    created() {
    },
  };
</script>