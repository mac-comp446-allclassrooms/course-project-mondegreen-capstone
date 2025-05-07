

<template>
  <div>
    <h1>Sign up</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="unField"/>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="pwField"/>
      </div>
      <div>
        <label for="passwordC">Confirm Password:</label>
        <input type="passwordC" id="passwordC"/>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        message: '',
      }
    },
    methods: {
      login(payload) {
        const path = 'http://localhost:5001/login';
        axios.post(path, payload)
        .then(function (response) {
          handleResponse(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      handleLogin() {
        un = this.unField.trim();
        pw = this.pwField.trim();

        if (this.verifyInput(un) && this.verifyInput(pw)) {
          const payload = {
            username: '',
            password: '',
          }
          this.login(payload);
        } else {
          this.message = 'Username and password must contain only alphanumeric characters!'
        }
      },
      handleResponse(response) {
        if (response.data.status === 'success') {
          this.message = 'logged in';
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
      }
    },
    created() {
    },
  };
</script>