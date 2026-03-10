#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. click on "open window" button, a window will be opened, after that switch to the main page and continue on the other script.
#4. click on "open tab" button, a new tab will be opened, after that switch to the main page and continue on the other script.
#5. Select option3 in dropdown.

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

        # 2️⃣ Click Open Window (new window opens)
        with page.expect_popup() as new_window:
            page.click("#openwindow")

        window = new_window.value
        window.wait_for_load_state()

        print("New window opened")

        # Close new window
        window.close()

        # Switch back to main page
        page.bring_to_front()

        # 3️⃣ Click Open Tab (new tab opens)
        with context.expect_page() as new_tab:
            page.click("#opentab")

        tab = new_tab.value
        tab.wait_for_load_state()

        print("New tab opened")

        # Close new tab
        tab.close()

        # Switch back to main page
        page.bring_to_front()

        # 4️⃣ Select option3 in dropdown
        page.select_option("#dropdown-class-example", "option3")

        print("Dropdown Option3 selected")

        page.wait_for_timeout(3000)

        browser.close()