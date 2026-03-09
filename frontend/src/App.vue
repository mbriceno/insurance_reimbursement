<template>
  <div>
    <router-view />
    <GlobalNotification />
  </div>
</template>

<script setup lang="ts">
import GlobalNotification from './components/GlobalNotification.vue';
import { onMounted } from 'vue';
import { useAuthStore } from './store/auth';

const authStore = useAuthStore();

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchMe();
  }
});
</script>
