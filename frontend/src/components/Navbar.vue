<template>
  <nav class="bg-blue-600 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <span class="text-white font-bold text-xl">InsuranceApp</span>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link v-if="authStore.isAuthenticated" to="/pets" class="text-white inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 border-transparent hover:border-white">
              My Pets
            </router-link>
            <router-link v-if="authStore.isAuthenticated" to="/claims/submit" class="text-white inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 border-transparent hover:border-white">
              Submit Claim
            </router-link>
          </div>
        </div>
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <span class="text-white text-sm">{{ authStore.user?.email }}</span>
            <button @click="handleLogout" class="text-white bg-blue-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-800">
              Logout
            </button>
          </div>
          <div v-else class="flex space-x-4">
            <router-link to="/login" class="text-white text-sm font-medium">Login</router-link>
            <router-link to="/register" class="text-white text-sm font-medium">Register</router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '../store/auth';

const authStore = useAuthStore();

async function handleLogout() {
  await authStore.logout();
}
</script>
