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


import os
import time
from playwright.sync_api import sync_playwright


def test_automation_practice():
    """
    Works locally in PyCharm (no pytest-playwright needed)
    AND in GitHub Actions CI (browser set via BROWSER env variable).
    """

    # Browser is set by CI via env var, defaults to chromium locally
    browser_name = os.environ.get("BROWSER", "chromium").lower()

    with sync_playwright() as p:

        launcher = {"chromium": p.chromium, "firefox": p.firefox, "webkit": p.webkit}
        browser = launcher.get(browser_name, p.chromium).launch(
            headless=True,   # headless=True for CI, change to False for local viewing
            slow_mo=300
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            # ─────────────────────────────────────────────────
            # STEP 1: Open the website
            # ─────────────────────────────────────────────────
            print("\n[STEP 1] Opening website...")
            page.goto("https://rahulshettyacademy.com/AutomationPractice/")
            page.wait_for_load_state("domcontentloaded")
            print("         ✔ Website loaded.")

            # ─────────────────────────────────────────────────
            # STEP 2: Maximise the window
            # ─────────────────────────────────────────────────
            print("[STEP 2] Maximising window...")
            page.set_viewport_size({"width": 1920, "height": 1080})
            print("         ✔ Window maximised.")

            # ─────────────────────────────────────────────────
            # STEP 3: Scroll chart sidebar below "Web Table Fixed Header"
            # ─────────────────────────────────────────────────
            print("[STEP 3] Scrolling chart sidebar below 'Web Table Fixed Header'...")
            page.evaluate("""
                const tableDiv = document.querySelector('.tableFixHead');
                if (tableDiv) { tableDiv.scrollTop = tableDiv.scrollHeight; }
            """)
            time.sleep(1)
            print("         ✔ Chart sidebar scrolled.")

            # ─────────────────────────────────────────────────
            # STEP 4: Scroll to iFrame Example, scroll inside iframe
            # ─────────────────────────────────────────────────
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

            # Scroll inside iframe via frame context (avoids cross-origin SecurityError)
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

            # ─────────────────────────────────────────────────
            # STEP 5: Click "View all courses" inside iframe
            # ─────────────────────────────────────────────────
            print("[STEP 5] Clicking 'View all courses' inside iframe...")
            iframe = page.frame_locator("iframe#courses-iframe")
            view_all_btn = iframe.locator(
                "a:has-text('View all courses'), button:has-text('View all courses'), .see-all-btn"
            )
            view_all_btn.first.wait_for(state="visible", timeout=15000)
            view_all_btn.first.scroll_into_view_if_needed()
            view_all_btn.first.click()
            time.sleep(3)
            print("         ✔ 'View all courses' clicked.")

            # ─────────────────────────────────────────────────
            # STEP 6: Type "Test" in "Search product names" field
            # ─────────────────────────────────────────────────
            print("[STEP 6] Typing 'Test' in 'Search product names' field...")
            search_field = iframe.locator(
                "input[placeholder*='Search product'], input[placeholder*='search product']"
            )
            search_field.first.wait_for(state="visible", timeout=10000)
            search_field.first.click()
            search_field.first.fill("Test")
            time.sleep(1)
            print("         ✔ Typed 'Test'.")

            # ─────────────────────────────────────────────────
            # STEP 7: "All Authors" combobox → select "Raymond"
            #   Radix UI combobox: aria-label="Filter by author"
            # ─────────────────────────────────────────────────
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

            # ─────────────────────────────────────────────────
            # STEP 8: "Recommended" combobox → select "Name(A-Z)"
            #   Radix UI: aria-label="Product sort options"
            #   FIX: 2 duplicate buttons — .last picks the visible active one
            # ─────────────────────────────────────────────────
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

            # ─────────────────────────────────────────────────
            # STEP 9: Verify and print no-match message
            # ─────────────────────────────────────────────────
            print("[STEP 9] Checking for 'No products match your current filters'...")
            no_match = iframe.locator("text=No products match your current filters")
            no_match.wait_for(state="visible", timeout=15000)
            result_text = no_match.inner_text()

            print(f"\n   >>> Message displayed: \"{result_text}\"\n")
            assert "No products match your current filters" in result_text, \
                f"Expected message not found! Got: '{result_text}'"
            print("         ✔ Assertion PASSED — Test Complete.\n")

        except Exception as e:
            screenshot_path = f"failure_{browser_name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n[FAIL] Error: {e}")
            print(f"       Screenshot saved as {screenshot_path}")
            raise

        finally:
            time.sleep(1)
            browser.close()
            print("[TEARDOWN] Browser closed.")