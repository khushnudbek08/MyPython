from playwright.sync_api import sync_playwright
from PIL import Image

URL = "https://www.scribd.com/document/674208625/JFT-模擬練習用紙-2"

images = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(URL)

    input("👉 Login qil va Enter bos")

    for i in range(15):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1000)

        path = f"page_{i}.png"
        page.screenshot(path=path, full_page=True)
        images.append(Image.open(path).convert("RGB"))

    browser.close()

images[0].save("final.pdf", save_all=True, append_images=images[1:])