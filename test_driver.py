from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)

driver.get("https://www.google.com")
print("標題：", driver.title)
driver.quit()
