#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. click on "open window" button, a window will be opened, after that switch to the main page and continue on the other script.
#4. click on "open tab" button, a new tab will be opened, after that switch to the main page and continue on the other script.
#5. Select option3 in dropdown.

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def test_newTabWindow():

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

            # STEP 2: Click Open Window
            print("[STEP 2] Clicking 'Open Window'...")

            open_window_btn = page.locator("#openwindow")
            open_window_btn.wait_for(state="visible")

            with page.expect_popup() as new_window:
                open_window_btn.click()

            window = new_window.value
            window.wait_for_load_state("domcontentloaded")

            print("✔ New window opened successfully")

            # Close new window
            print("[STEP 3] Closing new window...")
            window.close()
            print("✔ New window closed")

            # Switch back to main page
            page.bring_to_front()
            print("✔ Switched back to main page")

            # STEP 4: Click Open Tab
            print("[STEP 4] Clicking 'Open Tab'...")

            open_tab_btn = page.locator("#opentab")
            open_tab_btn.wait_for(state="visible")

            with context.expect_page() as new_tab:
                open_tab_btn.click()

            tab = new_tab.value
            tab.wait_for_load_state("domcontentloaded")

            print("✔ New tab opened successfully")

            # Close new tab
            print("[STEP 5] Closing new tab...")
            tab.close()
            print("✔ New tab closed")

            # Switch back to main page
            page.bring_to_front()
            print("✔ Switched back to main page")

            # STEP 6: Select option3 in dropdown
            print("[STEP 6] Selecting Option3 from dropdown...")

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