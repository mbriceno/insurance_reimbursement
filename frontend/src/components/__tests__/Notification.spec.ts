import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import GlobalNotification from '../GlobalNotification.vue';
import { useNotificationStore } from '../../store/notification';

describe('GlobalNotification.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renders notifications from the store', async () => {
    const store = useNotificationStore();
    store.add('Success message', 'success');
    
    const wrapper = mount(GlobalNotification);
    
    expect(wrapper.text()).toContain('Success message');
    expect(wrapper.find('.bg-green-50').exists()).toBe(true);
  });

  it('removes notification when close button is clicked', async () => {
    const store = useNotificationStore();
    store.add('Dismiss me', 'info');
    
    const wrapper = mount(GlobalNotification);
    const closeButton = wrapper.find('button');
    
    await closeButton.trigger('click');
    
    expect(store.notifications.length).toBe(0);
  });
});
