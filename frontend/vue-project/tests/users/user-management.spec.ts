import { test, expect } from '@playwright/test';
import { loginAsAdmin } from '../helpers/auth';

const BASE_URL = 'http://localhost:8081';

test.describe('UC11 + UC12 + UC13: User Management', () => {
    test('Complete user lifecycle: create, view, delete users', async ({ page }, testInfo) => {
        const uniqueSuffix = `${testInfo.project.name}-${testInfo.workerIndex}-${Date.now()}`;
        
        await loginAsAdmin(page);
        
        // uc12: add rescuer
        await page.goto(`${BASE_URL}/add-user`);

        // wait until form + roles are ready
        await expect(page.getByRole('heading', { name: 'Lisa Vabatahtlik' })).toBeVisible();
        await expect(page.locator('input[value="MANAGER"]')).toBeVisible();

        // fill in rescuer details
        const firstName = 'Test';
        const lastName = `User-${uniqueSuffix}`;
        const email = `testuser-${uniqueSuffix}@test.com`;

        await page.getByLabel('Eesnimi').fill(firstName);
        await page.getByLabel('Perekonnanimi').fill(lastName);
        await page.getByLabel('E-post').fill(email);
        await page.locator('#volunteer-phone').fill('5551234');

        // select role - manager
        await page.locator('input[value="MANAGER"]').check();

        
        // create user and wait for redirect to users list
        await Promise.all([
            page.waitForURL(`${BASE_URL}/users`),
            page.getByRole('button', { name: 'Loo' }).click(),
        ]);
        
        //  redirect to users list
        await expect(page).toHaveURL(`${BASE_URL}/users`);
        
        // uc11: view rescuers list
        await expect(page.getByRole('heading', { name: 'Vabatahtlikud' })).toBeVisible();
        
        // search for created user
        const searchInput = page.getByRole('textbox', { name: 'Otsi' }).first();
        await searchInput.fill(lastName);

        // verify user appears in filtered results
        const userRow = page.locator(`tr:has-text("${email}")`);
        await expect(userRow).toBeVisible();
        await expect(userRow).toContainText(firstName);

        
        // uc13: delete user 
        // create another user to delete
        await page.goto(`${BASE_URL}/add-user`);
        await page.getByLabel('Eesnimi').fill('ToDelete');
        await page.getByLabel('Perekonnanimi').fill(`Delete-${uniqueSuffix}`);
        await page.getByLabel('E-post').fill(`delete-${uniqueSuffix}@test.com`);
        await page.locator('input[value="NOT_MANAGER"]').check();
        await page.getByRole('button', { name: 'Loo' }).click();
        
        // search for the user to delete
        await searchInput.clear();
        await searchInput.fill('ToDelete');
        
        const deleteRow = page.locator(`tr:has-text("delete-${uniqueSuffix}@test.com")`);
        const deleteButton = deleteRow.locator('button[aria-label*="Delete"], button:has(svg)').last();
        
        if (await deleteButton.count() > 0) {
            await deleteButton.click();
            
            // confirm deletion if dialog appears (currently dont got it but will prepare for it)
            const confirmButton = page.locator('button:has-text("Kustuta"), button:has-text("Jah")');
            if (await confirmButton.count() > 0) {
                await confirmButton.click();
            }
            
            // verify user is removed
            await expect(deleteRow).not.toBeVisible();
        }
    });
});
