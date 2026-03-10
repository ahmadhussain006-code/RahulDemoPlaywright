#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. Open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. Below the "Web Table Fixed header" you will see a chart, on the chart, a side bar is showing, scroll down the side bar.
#4. Select option3 in the dropdown.

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def test_scrollSliderBar():

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

            # STEP 2: Scroll to Web Table Fixed Header section
            print("[STEP 2] Scrolling to 'Web Table Fixed Header' section...")

            header = page.locator("text=Web Table Fixed Header")
            header.wait_for(state="visible")
            header.scroll_into_view_if_needed()

            print("✔ Reached Web Table Fixed Header section")

            # STEP 3: Scroll the table scrollbar
            print("[STEP 3] Scrolling table scrollbar...")

            table = page.locator(".tableFixHead")
            table.wait_for(state="visible")
            table.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")

            print("✔ Table scrollbar scrolled successfully")

            # STEP 4: Select Option3 in dropdown
            print("[STEP 4] Selecting Option3 from dropdown...")

            dropdown = page.locator("#dropdown-class-example")
            dropdown.wait_for(state="visible")
            dropdown.select_option("option3")

            print("✔ Dropdown Option3 selected successfully")

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