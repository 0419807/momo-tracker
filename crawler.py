from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_momo_product_info(momo_id):
    url = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={momo_id}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x800")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        for _ in range(10):
            try:
                price_el = driver.find_element(By.CSS_SELECTOR, "ul.prdPrice li.special span")
                price_text = price_el.text.replace(',', '').replace('$', '').strip()
                price = int(''.join(filter(str.isdigit, price_text)))

                title = driver.title.split("-")[0].strip()
                driver.quit()
                return title, price, url
            except:
                time.sleep(1)

        driver.quit()
        return None, None, url

    except Exception as e:
        driver.quit()
        return None, None, url
