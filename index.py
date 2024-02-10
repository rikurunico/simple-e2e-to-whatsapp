from playwright.sync_api import Playwright, sync_playwright
from WPP_Whatsapp import Create


def login_to_website(page):
    page.goto("http://quotes.toscrape.com/login")
    page.get_by_label("Username").fill("dia")
    page.locator("#password").fill("aku")
    page.get_by_role("button", name="Login").click()


def navigate_to_quote_love(page):
    page.get_by_role("link", name="love").nth(1).click()


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    login_to_website(page)
    navigate_to_quote_love(page)

    page.screenshot(path="example-chromium.png", full_page=True)

    context.close()
    browser.close()


def catchQR(qrCode: str, asciiQR: str, attempt: int, urlCode: str):
    print(asciiQR)


def send_image_to_group(client, group_name, message, file_path):
    all_groups = client.getAllGroups(False)
    current_group = next(filter(lambda x: x.get("name") == group_name, all_groups), {})
    current_group_id = current_group.get("id", {}).get("_serialized")

    client.sendImage(current_group_id, filePath=file_path, caption=message)


def main():
    try:
        with sync_playwright() as playwright:
            run(playwright)

        print("Finish ss images")

        your_session_name = "nico-wpp-session"

        creator = Create(
            session=your_session_name,
            browser="firefox",
            catchQR=catchQR,
            logQR=True,
            headless=True,
        )

        client = creator.start()

        if creator.state != "CONNECTED":
            raise Exception(creator.state)

        group_name = "testing python"
        message = "Automated message from Python"
        file_path = "example-chromium.png"

        send_image_to_group(client, group_name, message, file_path)

        creator.sync_close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
