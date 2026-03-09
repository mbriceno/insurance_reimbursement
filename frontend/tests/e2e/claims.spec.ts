import { test, expect } from '@playwright/test';

test.describe('Claims', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake_token');
    });
    await page.route('**/api/auth/me/', async route => {
      await route.fulfill({ status: 200, json: { email: 'test@example.com', role: 'CUSTOMER' } });
    });
  });

  test('can submit a claim', async ({ page }) => {
    await page.route('**/api/pets/', async route => {
      await route.fulfill({ status: 200, json: [{ id: 1, name: 'Fido' }] });
    });
    await page.route('**/api/insurance/', async route => {
      await route.fulfill({ status: 200, json: [{ id: 10, pet_id: 1, policy_number: 'POL-1', is_active: true }] });
    });
    await page.route('**/api/claims/', async route => {
      await route.fulfill({ status: 201, json: { id: 100 } });
    });

    await page.goto('/claims/submit');
    await page.selectOption('select:near(:text("Select Pet"))', '1');
    await page.selectOption('select:near(:text("Select Insurance Policy"))', '10');
    await page.fill('input[type="number"]', '150.50');
    await page.fill('textarea', 'Vet visit for checkup');
    
    // File upload
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.click('input[type="file"]')
    ]);
    await fileChooser.setFiles({
      name: 'invoice.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('fake pdf content')
    });

    await page.click('button:has-text("Submit Claim")');
    await expect(page).toHaveURL(/.*pets/);
  });
});
