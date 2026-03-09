import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '../types';
import { apiPublic, apiAuth } from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const loading = ref(false);

  const accessToken = ref(localStorage.getItem('access_token'));
  const isAuthenticated = computed(() => !!accessToken.value);

  async function register(email: string, password: string) {
    loading.value = true;
    try {
      await apiPublic.post('/api/auth/register/', { email, password });
    } finally {
      loading.value = false;
    }
  }

  async function login(email: string, password: string) {
    loading.value = true;
    try {
      const response = await apiPublic.post('/api/token/', { email, password });
      const { access, refresh } = response.data;
      
      accessToken.value = access;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      await fetchMe();
      
      router.push('/pets');
    } finally {
      loading.value = false;
    }
  }

  async function fetchMe() {
    try {
      const response = await apiAuth.get('/api/auth/me/');
      user.value = response.data;
    } catch (error) {
      logout();
    }
  }

  async function refresh() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return logout();

    try {
      const response = await apiPublic.post('/api/token/refresh/', { refresh: refreshToken });
      const newAccess = response.data.access;
      accessToken.value = newAccess;
      localStorage.setItem('access_token', newAccess);
    } catch (error) {
      logout();
    }
  }

  function logout() {
    accessToken.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  }

  return { user, loading, isAuthenticated, register, login, fetchMe, refresh, logout };
});
