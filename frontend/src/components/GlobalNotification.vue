<template>
  <div class="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
    <transition-group 
      enter-active-class="transform ease-out duration-300 transition" 
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" 
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" 
      leave-active-class="transition ease-in duration-100" 
      leave-from-class="opacity-100" 
      leave-to-class="opacity-0"
    >
      <div 
        v-for="notification in notificationStore.notifications" 
        :key="notification.id"
        :class="[
          'p-4 rounded-lg shadow-lg flex items-center justify-between pointer-events-auto ring-1 ring-black ring-opacity-5',
          typeClasses[notification.type]
        ]"
      >
        <div class="flex-1 text-sm font-medium">
          {{ notification.message }}
        </div>
        <button 
          @click="notificationStore.remove(notification.id)" 
          class="ml-4 flex-shrink-0 inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
        >
          <span class="sr-only">Close</span>
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore, type NotificationType } from '../store/notification';

const notificationStore = useNotificationStore();

const typeClasses: Record<NotificationType, string> = {
  success: 'bg-green-50 border-green-200 text-green-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
};
</script>
