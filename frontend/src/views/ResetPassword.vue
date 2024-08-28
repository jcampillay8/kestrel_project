<template>
    <div class="container">
      <h2 class="text-center mt-5">Reset Password</h2>
      <form @submit.prevent="submitReset">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" v-model="email" required />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  
  const store = useStore();
  const email = ref('');
  
  const submitReset = () => {
    store.dispatch('requestPasswordReset', { email: email.value });
  };
  </script>
  