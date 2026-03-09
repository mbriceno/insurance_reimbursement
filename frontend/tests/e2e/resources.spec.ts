import { test, expect } from '@playwright/test';

test.describe('Resources', () => {
  test.beforeEach(async ({ page }) => {
    // Fake login
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake_token');
    });
    
    // Mock user profile
    await page.route('**/api/auth/me/', async route => {
      await route.fulfill({ status: 200, json: { email: 'test@example.com', role: 'CUSTOMER' } });
    });
  });

  test('can add a pet', async ({ page }) => {
    await page.route('**/api/pets/', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ status: 200, json: [] });
      } else if (route.request().method() === 'POST') {
        await route.fulfill({ status: 201, json: { id: 1, name: 'Fido', species: 'Dog' } });
      }
    });

    await page.goto('/pets');
    await page.click('button:has-text("Add Pet")');
    await page.fill('input[v-model="newPet.name"]', 'Fido');
    await page.fill('input[v-model="newPet.species"]', 'Dog');
    
    // Mock the reload after adding
    await page.route('**/api/pets/', async route => {
      await route.fulfill({ status: 200, json: [{ id: 1, name: 'Fido', species: 'Dog' }] });
    });
    
    await page.click('button:has-text("Save")');
    await expect(page.locator('.bg-white h3')).toContainText('Fido');
  });

  test('can create insurance policy', async ({ page }) => {
    await page.route('**/api/pets/', async route => {
        await route.fulfill({ status: 200, json: [{ id: 1, name: 'Fido', species: 'Dog' }] });
    });
    await page.route('**/api/insurance/', async route => {
        if (route.request().method() === 'GET') {
            await route.fulfill({ status: 200, json: [] });
        } else if (route.request().method() === 'POST') {
            await route.fulfill({ status: 201, json: { id: 10, pet_id: 1, policy_number: 'POL-1' } });
        }
    });

    await page.goto('/insurance/create');
    await page.selectOption('select', '1');
    await page.fill('input[v-model="form.policy_number"]', 'POL-123');
    await page.click('button:has-text("Create Policy")');
    
    await expect(page).toHaveURL(/.*pets\/1/);
  });
});
