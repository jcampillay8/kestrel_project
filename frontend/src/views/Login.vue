<template>
    <div class="container">
      <h2 class="text-center mt-5">Login</h2>
      <form @submit.prevent="submitLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" v-model="username" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  
  const store = useStore();
  const router = useRouter();
  const username = ref('');
  const password = ref('');
  
  const submitLogin = () => {
    store.dispatch('login', { username: username.value, password: password.value }).then(() => {
      router.push('/home');
    });
  };
  </script>
  