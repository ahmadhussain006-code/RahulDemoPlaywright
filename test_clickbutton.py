import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def test_clickbutton():

    # Browser will come from GitHub Actions matrix
    browser_name = os.getenv("BROWSER", "chromium")

    with sync_playwright() as p:

        print(f"\nRunning test on browser: {browser_name}")

        browser = getattr(p, browser_name).launch(
            headless=True,
            args=["--start-maximized"]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        page.set_default_timeout(60000)

        try:
            # STEP 1: Open website
            print("\n[STEP 1] Opening website...")

            page.goto(
                "https://rahulshettyacademy.com/AutomationPractice/",
                timeout=120000,
                wait_until="domcontentloaded"
            )

            print("✔ Website opened successfully")

            # STEP 2: Select Radio3
            print("[STEP 2] Selecting Radio3...")

            radio_btn = page.locator("input[value='radio3']")
            radio_btn.wait_for(state="visible")

            radio_btn.check()

            print("✔ Radio3 selected successfully")

            # Small wait for stability
            page.wait_for_timeout(2000)

        except PlaywrightTimeoutError as e:

            page.screenshot(
                path=f"failure_{browser_name}.png",
                full_page=True
            )

            print(f"\n[FAIL - TIMEOUT] Error: {e}")
            raise

        except Exception as e:

            page.screenshot(
                path=f"failure_{browser_name}.png",
                full_page=True
            )

            print(f"\n[FAIL] Error: {e}")
            raise

        finally:

            browser.close()

            print(f"[TEARDOWN] Browser closed for {browser_name}.")