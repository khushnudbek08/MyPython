from playwright.sync_api import sync_playwright

url = "https://www.scribd.com/document/674208625/JFT-模擬練習用紙-2"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")

    # Sahifani PDF qilib saqlash
    page.pdf(path="output.pdf", format="A4")

    browser.close()