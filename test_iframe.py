#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
# 1. Open this website- https://rahulshettyacademy.com/AutomationPractice/
# 2. Maximise the window
# 3. Below the "Web Table Fixed header" you will see a chart, on the chart a side bar is showing, scroll down the side bar.
# 4. At the middle of the page to the left corner you will see a text "iFrame Example" > below text you will see a iframe > scroll down the side bar.
# 5. Click on the "view all courses" button.
# 6. write "Test" in the "search product names" field.
# 7. Click on the dropdown button where field name is "All Authors" and select "Raymond".
# 8. Click on the dropdown button where field name is "Recommended" and select "Name(A-Z)".
# 9. This text should be shown "No products match your current filters". Print this text.


import time
import pytest
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_iframe(browser_name):
    with sync_playwright() as p:
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
            print(f"\nRunning test on browser: {browser_name}")

            # STEP 1: Open website
            print("\n[STEP 1] Opening website...")
            page.goto(
                "https://rahulshettyacademy.com/AutomationPractice/",
                wait_until="domcontentloaded",
                timeout=120000
            )
            print("         ✔ Website loaded.")

            # STEP 2: Maximise window
            print("[STEP 2] Maximising window...")
            print("         ✔ Window maximised.")

            # STEP 3: Scroll chart sidebar below 'Web Table Fixed Header'
            print("[STEP 3] Scrolling chart sidebar below 'Web Table Fixed Header'...")
            page.locator("text=Web Table Fixed header").scroll_into_view_if_needed()

            table_sidebar = page.locator(".tableFixHead")
            table_sidebar.wait_for(state="visible")
            table_sidebar.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
            time.sleep(1)

            print("         ✔ Chart sidebar scrolled.")

            # STEP 4: Scroll to iFrame Example and scroll inside iframe
            print("[STEP 4] Scrolling to 'iFrame Example' and scrolling iframe sidebar...")
            page.evaluate("""
                    const allEls = Array.from(document.querySelectorAll('*'));
                    const target = allEls.find(
                        el => el.childElementCount === 0 &&
                        el.innerText && el.innerText.trim() === 'iFrame Example'
                    );
                    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                """)
            time.sleep(1.5)

            page.wait_for_selector("iframe#courses-iframe", timeout=15000)

            courses_frame = (
                    page.frame(name="courses-iframe") or
                    next((f for f in page.frames if "courses-iframe" in (f.name or "")), None) or
                    next((f for f in page.frames if f.url != page.url and f != page.main_frame), None)
            )

            if courses_frame:
                courses_frame.evaluate("window.scrollTo(0, 500)")
                time.sleep(1)
                print("         ✔ iFrame sidebar scrolled.")
            else:
                print("         ⚠ iframe frame object not found, continuing...")

            iframe = page.frame_locator("iframe#courses-iframe")

            # STEP 5: Click 'View all courses' inside iframe
            print("[STEP 5] Clicking 'View all courses' inside iframe...")
            view_all_btn = iframe.locator(
                "a:has-text('View all courses'), button:has-text('View all courses'), .see-all-btn"
            )
            view_all_btn.first.wait_for(state="visible", timeout=15000)
            view_all_btn.first.scroll_into_view_if_needed()
            view_all_btn.first.click()
            time.sleep(3)
            print("         ✔ 'View all courses' clicked.")

            # STEP 6: Type 'Test' in 'Search product names' field
            print("[STEP 6] Typing 'Test' in 'Search product names' field...")
            search_field = iframe.locator(
                "input[placeholder*='Search product'], input[placeholder*='search product']"
            )
            search_field.first.wait_for(state="visible", timeout=10000)
            search_field.first.click()
            search_field.first.fill("Test")
            time.sleep(1)
            print("         ✔ Typed 'Test'.")

            # STEP 7: Click 'All Authors' dropdown and select 'Raymond'
            print("[STEP 7] Clicking 'All Authors' combobox and selecting 'Raymond'...")
            authors_btn = iframe.locator("button[aria-label='Filter by author']")
            authors_btn.scroll_into_view_if_needed()
            authors_btn.wait_for(state="visible", timeout=10000)
            authors_btn.click()
            time.sleep(1)

            raymond_option = iframe.locator("[role='option']:has-text('Raymond')")
            raymond_option.first.wait_for(state="visible", timeout=10000)
            raymond_option.first.click()
            time.sleep(1)
            print("         ✔ 'Raymond' selected.")

            # STEP 8: Click 'Recommended' dropdown and select 'Name(A-Z)'
            print("[STEP 8] Clicking 'Recommended' combobox and selecting 'Name(A-Z)'...")
            sort_btn = iframe.locator(
                "button[aria-label='Product sort options'][data-state='closed']"
            ).last
            sort_btn.scroll_into_view_if_needed()
            sort_btn.wait_for(state="visible", timeout=10000)
            sort_btn.click()
            time.sleep(1)

            name_az_option = iframe.locator("[role='option']:has-text('Name')")
            name_az_option.first.wait_for(state="visible", timeout=10000)
            name_az_option.first.click()
            time.sleep(1.5)
            print("         ✔ 'Name(A-Z)' selected.")

            # STEP 9: Verify and print no-match message
            print("[STEP 9] Checking for 'No products match your current filters'...")
            no_match = iframe.locator("text=No products match your current filters")
            no_match.wait_for(state="visible", timeout=15000)
            result_text = no_match.inner_text()

            print(f'\n   >>> Message displayed: "{result_text}"\n')
            assert "No products match your current filters" in result_text, \
                f"Expected message not found! Got: '{result_text}'"

            print("         ✔ Assertion PASSED — Test Complete.\n")

        except PlaywrightTimeoutError as e:
            page.screenshot(path=f"failure_{browser_name}.png", full_page=True)
            print(f"\n[FAIL - TIMEOUT] Error: {e}")
            raise

        except Exception as e:
            page.screenshot(path=f"failure_{browser_name}.png", full_page=True)
            print(f"\n[FAIL] Error: {e}")
            raise

        finally:
            browser.close()
            print(f"[TEARDOWN] Browser closed for {browser_name}.")