#Think and act like you are a senior software tester. Write a script to automate this website on the PyCharm framework using Playwright with Python.
#1. open this website- https://rahulshettyacademy.com/AutomationPractice/
#2. Maximise the window
#3. click on the "Alert" button > a pop will appear from the top of the page > click on the "ok" button.
#4. write "Hussain text" in the "enter you name" field.
#5. click on the "confirm" button  > a pop will appear from the top of the page > click on the "ok" button.


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

        # Handle Alert popup
        page.once("dialog", lambda dialog: dialog.accept())

        # 2️⃣ Click Alert button
        page.click("#alertbtn")

        print("Alert handled successfully")

        # 3️⃣ Enter name
        page.fill("#name", "Hussain text")

        # Handle Confirm popup
        page.once("dialog", lambda dialog: dialog.accept())

        # 4️⃣ Click Confirm button
        page.click("#confirmbtn")

        print("Confirm popup handled successfully")

        page.wait_for_timeout(3000)

        browser.close()