FROM mcr.microsoft.com/playwright/python:latest

# 安裝系統工具（Render 必備）
RUN apt-get update && apt-get install -y unzip curl && apt-get clean

# 設定工作目錄
WORKDIR /app
COPY . /app

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# Render 預設埠為 10000，可改成環境變數或固定值
ENV PORT=10000

# 執行 Flask
CMD ["python", "app.py"]

