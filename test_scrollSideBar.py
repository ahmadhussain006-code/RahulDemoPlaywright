#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. Open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. Below the "Web Table Fixed header" you will see a chart, on the chart, a side bar is showing, scroll down the side bar.
#4. Select option3 in the dropdown.

from playwright.sync_api import sync_playwright


def test_practice():

    with sync_playwright() as p:

        # Launch browser maximized
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        # Remove viewport restriction
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        page.set_default_timeout(60000)

        # 1️⃣ Open website
        page.goto(
            "https://rahulshettyacademy.com/AutomationPractice/",
            timeout=120000,
            wait_until="domcontentloaded"
        )

        # 2️⃣ Scroll to Web Table Fixed Header section
        page.locator("text=Web Table Fixed Header").scroll_into_view_if_needed()

        # 3️⃣ Scroll the table scrollbar
        table = page.locator(".tableFixHead")

        # Scroll down inside the table
        table.evaluate("el => el.scrollTop = el.scrollHeight")

        print("Table scrollbar scrolled")

        # 4️⃣ Select Option3 in dropdown
        page.select_option("#dropdown-class-example", "option3")

        print("Dropdown Option3 selected")

        page.wait_for_timeout(3000)

        browser.close()