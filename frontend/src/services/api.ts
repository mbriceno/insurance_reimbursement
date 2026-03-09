import axios from 'axios';
import { useNotificationStore } from '../store/notification';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiPublic = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiAuth = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiAuth.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

function handleGlobalError(error: any) {
  const notificationStore = useNotificationStore();
  const status = error.response?.status;
  const detail = error.response?.data?.detail || error.message;

  if (status === 401) {
    // 401 is handled by refresh logic, but if refresh fails, we notify
    if (error.config?._retry_failed) {
        notificationStore.add('Session expired. Please login again.', 'error');
    }
  } else if (status === 403) {
    notificationStore.add('You do not have permission to perform this action.', 'error');
  } else if (status === 400) {
    notificationStore.add(`Bad Request: ${detail}`, 'error');
  } else if (status >= 500) {
    notificationStore.add('A server error occurred. Please try again later.', 'error');
  } else {
    notificationStore.add(`Error: ${detail}`, 'error');
  }
}

apiAuth.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        try {
          const response = await apiPublic.post('/api/token/refresh/', { refresh: refreshToken });
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return apiAuth(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          originalRequest._retry_failed = true;
          handleGlobalError(error);
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }
    handleGlobalError(error);
    return Promise.reject(error);
  }
);

apiPublic.interceptors.response.use(
  (response) => response,
  (error) => {
    handleGlobalError(error);
    return Promise.reject(error);
  }
);
