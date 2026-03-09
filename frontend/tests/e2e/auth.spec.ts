import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('successful registration redirects to login', async ({ page }) => {
    await page.route('**/api/auth/register/', async route => {
      await route.fulfill({ status: 201, json: { email: 'test@example.com' } });
    });

    await page.goto('/register');
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'password123');
    await page.locator('input[type="password"]').nth(1).fill('password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*login/);
    await expect(page.locator('.bg-green-50')).toContainText('Registration successful');
  });

  test('successful login redirects to pets', async ({ page }) => {
    await page.route('**/api/token/', async route => {
      await route.fulfill({ status: 200, json: { access: 'fake_access', refresh: 'fake_refresh' } });
    });
    await page.route('**/api/auth/me/', async route => {
      await route.fulfill({ status: 200, json: { email: 'test@example.com', role: 'CUSTOMER' } });
    });

    await page.goto('/login');
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*pets/);
  });
});
