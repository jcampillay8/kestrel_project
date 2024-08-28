<template>
    <div class="container">
      <h2 class="text-center mt-5">Set New Password</h2>
      <form @submit.prevent="submitNewPassword">
        <div class="mb-3">
          <label for="password" class="form-label">New Password</label>
          <input type="password" class="form-control" id="password" v-model="password" required />
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Confirm Password</label>
          <input type="password" class="form-control" id="password2" v-model="password2" required />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRoute, useRouter } from 'vue-router';
  
  const store = useStore();
  const route = useRoute();
  const router = useRouter();
  const password = ref('');
  const password2 = ref('');
  
  const submitNewPassword = () => {
    if (password.value !== password2.value) {
      alert('Passwords do not match');
      return;
    }
  
    const uidb64 = route.params.uidb64;
    const token = route.params.token;
  
    store.dispatch('setNewPassword', {
      uidb64: uidb64,
      token: token,
      password: password.value,
      password2: password2.value,
    }).then(() => {
      router.push('/login');
    });
  };
  </script>
  