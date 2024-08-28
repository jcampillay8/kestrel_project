<template>
    <div class="container">
      <h2 class="text-center mt-5">Register</h2>
      <form @submit.prevent="submitRegister">
        <div class="mb-3">
          <label for="firstName" class="form-label">First Name</label>
          <input type="text" class="form-control" id="firstName" v-model="firstName" required />
        </div>
        <div class="mb-3">
          <label for="lastName" class="form-label">Last Name</label>
          <input type="text" class="form-control" id="lastName" v-model="lastName" required />
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" v-model="username" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" v-model="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  
  const store = useStore();
  const router = useRouter();
  const firstName = ref('');
  const lastName = ref('');
  const username = ref('');
  const email = ref('');
  const password = ref('');
  
  const submitRegister = () => {
    store.dispatch('register', {
      first_name: firstName.value,
      last_name: lastName.value,
      username: username.value,
      email: email.value,
      password: password.value
    }).then(() => {
      router.push('/login');
    });
  };
  </script>
  