#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. Click on the text link "Get Shortlisted...." right side on the top.> a new tab will be opened, after that switch to the main page and continue on the other script.
#4. Select option3 in dropdown.

from playwright.sync_api import sync_playwright


def test_practice():

    with sync_playwright() as p:

        # Launch browser maximized
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        page.set_default_timeout(60000)

        # Open website
        page.goto(
            "https://rahulshettyacademy.com/AutomationPractice/",
            timeout=120000,
            wait_until="domcontentloaded"
        )

        # Scroll to the top (important fix)
        page.evaluate("window.scrollTo(0,0)")

        # Click the top-right text link
        link = page.get_by_text("Get Shortlisted by Recruiters - Take QA Skill Assessments on TechSmartHire")

        with context.expect_page() as new_tab:
            link.click()

        tab = new_tab.value
        tab.wait_for_load_state()

        print("New tab opened")

        # Close the new tab
        tab.close()

        # Switch back to main page
        page.bring_to_front()

        # Select Option3 in dropdown
        page.select_option("#dropdown-class-example", "option3")

        print("Dropdown Option3 selected")

        page.wait_for_timeout(3000)

        browser.close()