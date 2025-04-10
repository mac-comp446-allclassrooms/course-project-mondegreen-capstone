<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password"/>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>
