import { test, expect } from '@playwright/test';
import { loginAsAdmin } from '../helpers/auth';


const BASE_URL = 'http://localhost:8081';

test('UC-T1: succesful registration of a new cat', async ({page}) => {
    await loginAsAdmin(page);

    await page.goto(`${BASE_URL}/add-cat`)

    //system shows empty form
    await expect(page.getByRole('heading', { name: 'Kassid', exact: true})).toBeVisible();
    //entering basic cat fields
    //name
    await page.getByLabel('Kassi nimi').fill('Mimi');
    //sex
    await page.locator('input[name="cat-sex"][value="female"]').check()
    //birthdate
    await page.locator('#cat-birth-date').fill('2020-01-01');
    //original colony
    const hasSupilinn = await page.locator('#cat-colony >> option', { hasText: 'Supilinn' }).count();

    if (hasSupilinn > 0) {
        // Colony exists → select it
        await page.selectOption('#cat-colony', { label: 'Supilinn' });
    } else {
        // Colony doesn't exist → click the + button
        await page.locator('button.accept.aspect-square').click();
        await page.locator('#new-colony-name').fill('Supilinn');
    }
    //chip nr
    await page.fill('#cat-chip-id', '123456789012345');

    //status
    await page.selectOption('#cat-status', 'ACTIVE')
    //KK from
    await page.locator('#cat-home-since').fill('2024-10-01');
    //Kodukal
    await page.locator('input[name="cat-on-homepage"][value="true"]').check()
    //Manager
    await page.selectOption('#cat-manager', { label: 'caro m' });
    //Foster home name
    await page.locator('#foster-home-name').fill('Hoiukodu1');
    //Create it
    await page.locator('button[type="submit"]').click();


    //POST-CONDITIONS:
    //check if goes to the right page
    await expect(page).toHaveURL(/\/cats\/\d+$/);

});

