from app.models.schemas import BMI
from playwright.async_api import async_playwright


async def get_bmi(*, age, height_cm, weight_kg):
    """
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=False to see the browser
        context = await browser.new_context()
        page = await context.new_page()

        # Go to BMI Calculator page
        await page.goto("https://www.calculator.net/bmi-calculator.html")

        # Set units to metric
        await page.locator("a", has_text="Metric Units").first.click()

        # Fill the form
        await page.fill('input[name="cage"]', str(age))
        await page.fill('input[name="cheightmeter"]', str(height_cm))
        await page.fill('input[name="ckg"]', str(weight_kg))

        # Submit
        await page.click('input[type="submit"]')

        # Wait for result to load
        await page.wait_for_selector('.rightresult')

        # Extract BMI value and category from result block
        result_block = await page.text_content('.rightresult')

        if result_block:
            # Example: "BMI = 22.9 kg/m2 (Normal)"
            import re
            bmi_pattern = (
                r"BMI\s*="        # Match "BMI =" with optional spaces before/after the equals sign
                r"\s*([\d.]+)"    # Capture the BMI number (digits + optional decimal), e.g., "22.9"
                r"\s*kg/m2"       # Match the units "kg/m2", possibly with spaces before
                r"\s*\(([^)]+)\)" # Capture the BMI category inside parentheses, e.g., "(Normal)"
            )
            match = re.search(bmi_pattern, result_block)

            if match:
                bmi_value = match.group(1)      # Captures the BMI number, e.g., "22.9"
                bmi_category = match.group(2)   # Captures the category, e.g., "Normal"

                print(f"BMI Value: {bmi_value}")
                print(f"Category: {bmi_category}")
            else:
                print("Could not find BMI value and category in the result text.")
        else:
            print("No result found on the page.")

        await browser.close()

        return BMI(age=age, height=height_cm, weight=weight_kg, bmi=bmi_value, category=bmi_category)