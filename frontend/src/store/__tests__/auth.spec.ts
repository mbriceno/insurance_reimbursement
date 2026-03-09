import { setActivePinia, createPinia } from 'pinia';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from '../auth';
import { apiPublic, apiAuth } from '../../services/api';

vi.mock('../../services/api', () => ({
  apiPublic: {
    post: vi.fn(),
  },
  apiAuth: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

vi.mock('../../router', () => ({
  default: {
    push: vi.fn(),
  },
}));

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('registers a new user', async () => {
    const store = useAuthStore();
    (apiPublic.post as any).mockResolvedValueOnce({ data: { email: 'test@example.com', role: 'CUSTOMER' } });

    await store.register('test@example.com', 'password123');

    expect(apiPublic.post).toHaveBeenCalledWith('/api/auth/register/', {
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('logs in a user and sets tokens', async () => {
    const store = useAuthStore();
    (apiPublic.post as any).mockResolvedValueOnce({ 
      data: { access: 'access_token', refresh: 'refresh_token' } 
    });
    (apiAuth.get as any).mockResolvedValueOnce({ 
      data: { email: 'test@example.com', role: 'CUSTOMER' } 
    });

    await store.login('test@example.com', 'password123');

    expect(store.isAuthenticated).toBe(true);
    expect(localStorage.getItem('access_token')).toBe('access_token');
    expect(localStorage.getItem('refresh_token')).toBe('refresh_token');
    expect(store.user?.email).toBe('test@example.com');
  });

  it('logs out a user and clears storage', () => {
    const store = useAuthStore();
    localStorage.setItem('access_token', 'token');
    store.user = { id: '1', email: 't@t.com', username: 'u', role: 'CUSTOMER' };

    store.logout();

    expect(store.isAuthenticated).toBe(false);
    expect(store.user).toBeNull();
    expect(localStorage.getItem('access_token')).toBeNull();
  });
});
