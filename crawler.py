from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_momo_product_info(momo_id):
    url = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={momo_id}"
    print(f"🌐 開始打開網頁：{url}", flush=True)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280x800")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get(url)
        print("🌍 網頁已載入", flush=True)

        # ✅ 等待價格出現
        try:
            price_el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.prdPrice li.special span"))
            )
            price_text = price_el.text.strip().replace(',', '').replace('$', '')
            price = int(''.join(filter(str.isdigit, price_text)))

            title = driver.title.split("-")[0].strip()
            print(f"✅ 成功抓到：{title} / {price}", flush=True)

            driver.quit()
            return title, price, url

        except Exception as e:
            print(f"❌ 等待價格元素失敗：{e}", flush=True)
            driver.quit()
            return None, None, url

    except Exception as e:
        print(f"❌ Selenium 發生錯誤：{e}", flush=True)
        driver.quit()
        return None, None, url
