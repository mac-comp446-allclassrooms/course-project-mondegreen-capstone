<script>
export default {
  methods: {
    handleLogin() {
      alert('Form submitted');
    }
  }
};
</script>

<template>
  <div>
    <h1>Sign up</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password"/>
      </div>
      <div>
        <label for="passwordC">Confirm Password:</label>
        <input type="passwordC" id="passwordC"/>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>
