#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. Click on the text link "Get Shortlisted...." right side on the top.> a new tab will be opened, after that switch to the main page and continue on the other script.
#4. Select option3 in dropdown.

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def test_clickTestlink():

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

            # STEP 2: Scroll to top
            print("[STEP 2] Scrolling to top...")
            page.evaluate("window.scrollTo(0, 0)")
            print("✔ Scrolled to top")

            # STEP 3: Click the top-right text link and handle new tab
            print("[STEP 3] Clicking recruiter link and opening new tab...")

            link = page.get_by_text(
                "Get Shortlisted by Recruiters - Take QA Skill Assessments on TechSmartHire"
            )
            link.wait_for(state="visible")

            with context.expect_page() as new_tab:
                link.click()

            tab = new_tab.value
            tab.wait_for_load_state("domcontentloaded")

            print("✔ New tab opened successfully")

            # STEP 4: Close new tab
            print("[STEP 4] Closing new tab...")
            tab.close()
            print("✔ New tab closed")

            # STEP 5: Switch back to main page
            print("[STEP 5] Switching back to main page...")
            page.bring_to_front()
            print("✔ Switched back to main page")

            # STEP 6: Select Option3 in dropdown
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