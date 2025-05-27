from playwright.sync_api import sync_playwright
import re

def get_momo_product_info(momo_id):
    url = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={momo_id}"
    print(f"🌐 開始打開網頁：{url}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="zh-TW"
        )
        page = context.new_page()

        try:
            page.goto(url, timeout=60000)
            page.wait_for_timeout(2000)  # 初步等待

            # 嘗試抓價格的 selector（多備援）
            selectors = [
                "#goodsDetail .prdPrice li.special span",  # 特價
                "#goodsDetail .prdPrice li span",          # 原價
                ".priceArea .special",                     # 備援
                "li.special > span",                       # 簡化
            ]

            price = None
            for selector in selectors:
                try:
                    el = page.wait_for_selector(selector, timeout=3000)
                    text = el.inner_text().replace(",", "").replace("$", "").strip()
                    print(f"🎯 抓到價格字串：{text}")
                    if text and re.match(r"^\d+$", text):
                        price = int(text)
                        break
                except:
                    continue

            # 擷取商品名稱
            title = page.title()
            name = title.split("-")[0].strip()

            # 若沒抓到價格，輔助 debug
            if not price:
                print("❌ 無法擷取價格，開始輔助診斷...")
                page.screenshot(path="momo_debug.png", full_page=True)
                with open("momo_debug.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
                return None, None, url

            print(f"✅ 成功擷取：{name} / {price}")
            return name, price, url

        except Exception as e:
            print(f"❌ 發生錯誤：{e}")
            return None, None, url

        finally:
            browser.close()
