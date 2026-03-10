from playwright.sync_api import sync_playwright


def test_practice():

    with sync_playwright() as p:

        # Launch browser in maximized mode
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        # Create context without viewport restriction
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Increase default timeout
        page.set_default_timeout(60000)

        # Open website
        page.goto(
            "https://rahulshettyacademy.com/AutomationPractice/",
            timeout=120000,
            wait_until="domcontentloaded"
        )

        # Select Radio Button - Radio3
        page.check("input[value='radio3']")

        print("Radio3 selected successfully")

        # Wait few seconds to see result
        page.wait_for_timeout(3000)

        browser.close()