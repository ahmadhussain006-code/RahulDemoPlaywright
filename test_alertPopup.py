#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. click on the "Alert" button > a pop will appear from the top of the page > click on the "ok" button.
#4. write "Hussain text" in the "enter you name" field.
#5. click on the "confirm" button  > a pop will appear from the top of the page > click on the "ok" button.


import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def test_alertPopup():

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

            # STEP 2: Handle alert popup
            print("[STEP 2] Handling alert popup...")

            page.once("dialog", lambda dialog: dialog.accept())

            alert_btn = page.locator("#alertbtn")
            alert_btn.wait_for(state="visible")
            alert_btn.click()

            print("✔ Alert handled successfully")

            # STEP 3: Enter name
            print("[STEP 3] Entering name in input field...")

            name_field = page.locator("#name")
            name_field.wait_for(state="visible")
            name_field.fill("Hussain text")

            print("✔ Name entered successfully")

            # STEP 4: Handle confirm popup
            print("[STEP 4] Handling confirm popup...")

            page.once("dialog", lambda dialog: dialog.accept())

            confirm_btn = page.locator("#confirmbtn")
            confirm_btn.wait_for(state="visible")
            confirm_btn.click()

            print("✔ Confirm popup handled successfully")

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