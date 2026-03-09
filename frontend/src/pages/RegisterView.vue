<template>
  <div>
    <h2 class="text-center text-2xl font-bold mb-6">Register</h2>
    <form @submit.prevent="handleRegister" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input 
          v-model="email" 
          type="email" 
          required 
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input 
          v-model="password" 
          type="password" 
          required 
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Confirm Password</label>
        <input 
          v-model="confirmPassword" 
          type="password" 
          required 
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>
      <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
      <button 
        type="submit" 
        :disabled="authStore.loading"
        class="w-full bg-blue-600 text-white rounded-md p-2 hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ authStore.loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <div class="mt-4 text-center">
      <router-link to="/login" class="text-blue-600 text-sm">Already have an account? Login</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../store/auth';
import { useNotificationStore } from '../store/notification';
import router from '../router';

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');

const authStore = useAuthStore();
const notificationStore = useNotificationStore();

async function handleRegister() {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match';
    return;
  }
  
  error.value = '';
  try {
    await authStore.register(email.value, password.value);
    notificationStore.add('Registration successful! Please login.', 'success');
    router.push('/login');
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Registration failed';
  }
}
</script>
