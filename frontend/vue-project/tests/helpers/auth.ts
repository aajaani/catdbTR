import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:8081';

export async function loginAsAdmin(page) {
    await page.goto(`${BASE_URL}/login`);

    await page.getByLabel('E-mail').fill('admin');
    await page.getByLabel('Parool').fill('admin12345');
    await page.getByRole('button', { name: /logi sisse/i}).click();

    await expect(page).toHaveURL(`${BASE_URL}/`);
}

export async function logout(page: Page) {
    await page.locator('button:has-text("Logi valja")').click();
    await expect(page).toHaveURL(`${BASE_URL}/login`);
}