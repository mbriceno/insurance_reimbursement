import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('unauthenticated user sees login/register', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('nav')).toContainText('Login');
    await expect(page.locator('nav')).toContainText('Register');
    await expect(page.locator('nav')).not.toContainText('Logout');
  });

  test('authenticated user sees logout and profile', async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake_token');
    });
    await page.route('**/api/auth/me/', async route => {
      await route.fulfill({ status: 200, json: { email: 'user@example.com', role: 'CUSTOMER' } });
    });

    await page.goto('/pets');
    await expect(page.locator('nav')).toContainText('Logout');
    await expect(page.locator('nav')).toContainText('user@example.com');
  });
});
