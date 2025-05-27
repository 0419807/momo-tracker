from playwright.sync_api import sync_playwright

def get_momo_product_info(momo_id):
    url = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={momo_id}"
    print(f"🌐 打開：{url}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        selectors = [
            "#goodsDetail .prdPrice li.special span",
            "#goodsDetail .prdPrice li span",
            ".priceArea .special"
        ]

        price_text = None
        for selector in selectors:
            try:
                el = page.query_selector(selector)
                if el:
                    text = el.inner_text().replace(",", "").replace("$", "").strip()
                    if text.isdigit():
                        price_text = int(text)
                        break
            except:
                continue

        name = page.title().split("-")[0].strip() if price_text else None
        browser.close()

        if price_text:
            print(f"✅ 擷取成功：{name} / {price_text}")
            return name, price_text, url
        else:
            print("❌ 價格抓不到")
            return None, None, url
