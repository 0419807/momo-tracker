FROM python:3.10-slim

# 安裝 Chrome 相關工具
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 設定 Headless Chrome 的環境變數
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 設定語系（有些網站會依語系返回不同內容）
ENV LANG C.UTF-8

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
