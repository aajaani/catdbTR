import { test, expect } from '@playwright/test';
import { loginAsAdmin } from '../helpers/auth';

const BASE_URL = 'http://localhost:8081';

test.describe('UC1 + UC2: Cat Registration and Browsing', () => {
    test('cat lifecycle: create, view, filter', async ({ page }, testInfo) => {
        const uniqueSuffix = `${testInfo.project.name}-${testInfo.workerIndex}-${Date.now()}`;
        
        await loginAsAdmin(page);
        
        // uc1 part: create multiple cats for testing
        // first, create manager "caro m" with unique email
        await page.goto(`${BASE_URL}/add-user`);
        await page.getByLabel('Eesnimi').fill('caro');
        await page.getByLabel('Perekonnanimi').fill('m');
        await page.getByLabel('E-post').fill(`caro-${uniqueSuffix}@example.com`);
        await page.getByRole('button', { name: 'Loo' }).click();
        
        // create first cat - active status
        await page.goto(`${BASE_URL}/add-cat`);
        
        // system shows empty form
        await expect(page.getByRole('heading', { name: 'Kassid', exact: true })).toBeVisible();
        
        // entering basic cat fields
        // name (unique per run)
        const catName1 = `Mimi-${uniqueSuffix}`;
        await page.getByLabel('Kassi nimi').fill(catName1);
        // sex
        await page.locator('input[name="cat-sex"][value="female"]').check();
        // birthdate
        await page.locator('#cat-birth-date').fill('2020-01-01');
        // original colony
        const hasSupilinn = await page
            .locator('#cat-colony >> option', { hasText: 'Supilinn' })
            .count();
        
        if (hasSupilinn > 0) {
            // colony exists → select it
            await page.selectOption('#cat-colony', { label: 'Supilinn' });
        } else {
            // colony doesn't exist → click the + button
            await page.locator('button.accept.aspect-square').click();
            await page.locator('#new-colony-name').fill('Supilinn');
        }
        // chip nr
        await page.fill('#cat-chip-id', '123456789012345');
        
        // status
        await page.selectOption('#cat-status', 'ACTIVE');
        // kk from
        await page.locator('#cat-home-since').fill('2024-10-01');
        // kodukal
        await page.locator('input[name="cat-on-homepage"][value="true"]').check();
        // manager
        await page.selectOption('#cat-manager', { label: 'caro m' });
        // foster home name
        await page.locator('#foster-home-name').fill('Hoiukodu1');
        // create it
        await page.locator('button[type="submit"]').click();
        
        // post-conditions:
        // check if goes to the right page
        await expect(page).toHaveURL(/\/cats\/\d+$/);
        
        // create second cat - adopted status for filtering
        await page.goto(`${BASE_URL}/add-cat`);
        const catName2 = `Felix-${uniqueSuffix}`;
        await page.getByLabel('Kassi nimi').fill(catName2);
        await page.locator('input[name="cat-sex"][value="male"]').check();
        await page.selectOption('#cat-status', 'ADOPTED');
        await page.locator('#foster-home-name').fill('Hoiukodu2');
        await page.locator('button[type="submit"]').click();
        
        // uc2 part: browse and filter cats
        await page.goto(`${BASE_URL}/cats`);
        
        // verify cat list loads with our cats
        await expect(page.getByRole('heading', { name: 'Kassid', exact: true })).toBeVisible();
        const catTable = page.locator('table');
        await expect(catTable).toBeVisible();
        
        // test search functionality
        const searchInput = page.getByRole('textbox', { name: 'Otsi' }).first();
        await searchInput.fill(catName1);
        
        // verify search results show only mimi
        await expect(page.locator(`tr:has-text("${catName1}")`)).toBeVisible();
        await expect(page.locator(`tr:has-text("${catName2}")`)).not.toBeVisible();
        
        // clear search
        await searchInput.clear();
        
        // test status filter 
        
        const statusFilter = page.locator('[data-filter="status"]').first();
        if (await statusFilter.count() > 0) {
            await statusFilter.click();
            await page.locator('text=Uues kodus').click(); // adopted status
            
            // verify only adopted cat shows
            await expect(page.locator(`tr:has-text("${catName2}")`)).toBeVisible();
            await expect(page.locator(`tr:has-text("${catName1}")`)).not.toBeVisible();
        }
        
    });
});
