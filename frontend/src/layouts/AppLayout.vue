<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar v-if="showNavbar" />
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import Navbar from '../components/Navbar.vue';

// Navbar might be conditional based on auth later
const showNavbar = computed(() => true);
</script>
