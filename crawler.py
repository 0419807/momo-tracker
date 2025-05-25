import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_momo_product_info(momo_id):
    url = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={momo_id}"
    print(f"🌐 開始打開網頁：{url}", flush=True)

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280x800")

    driver = uc.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        time.sleep(2)

        # 嘗試多個 selector
        selectors = [
            "ul.prdPrice li.special span",
            "#goodsPrice",
            "span.priceArea span"
        ]
        for selector in selectors:
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                price_text = el.text.strip().replace(',', '').replace('$', '')
                price = int(''.join(filter(str.isdigit, price_text)))
                title = driver.title.split("-")[0].strip()

                print(f"✅ 成功抓到：{title} / {price}", flush=True)
                driver.quit()
                return title, price, url
            except:
                continue

        print("❌ 所有 selector 都抓不到價格", flush=True)
        driver.quit()
        return None, None, url

    except Exception as e:
        print(f"❌ Selenium 發生錯誤：{e}", flush=True)
        driver.quit()
        return None, None, url
