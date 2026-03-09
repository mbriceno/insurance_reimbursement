import { defineStore } from 'pinia';
import { ref } from 'vue';

export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface Notification {
  id: number;
  message: string;
  type: NotificationType;
}

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([]);
  let nextId = 1;

  function add(message: string, type: NotificationType = 'info', timeout = 5000) {
    const id = nextId++;
    notifications.value.push({ id, message, type });

    if (timeout > 0) {
      setTimeout(() => {
        remove(id);
      }, timeout);
    }
  }

  function remove(id: number) {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  }

  return { notifications, add, remove };
});
