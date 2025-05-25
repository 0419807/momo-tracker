from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
import re
from apscheduler.schedulers.background import BackgroundScheduler
import time
from crawler import get_momo_product_info

app = Flask(__name__)

# -------------------- 資料庫操作 --------------------

def init_db():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracked (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            url TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_tracked(name, price, url):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO tracked (name, price, url) VALUES (?, ?, ?)", (name, price, url))
    conn.commit()
    conn.close()

def delete_tracked(product_id):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("DELETE FROM tracked WHERE id = ?", (product_id,))
    c.execute("DELETE FROM price_history WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_all_tracked():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("SELECT id, name, price, url FROM tracked")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "price": r[2], "url": r[3]} for r in rows]

# -------------------- 自動更新價格 --------------------

def update_prices():
    print("\U0001f501 開始更新 Momo 價格...")
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("SELECT id, url FROM tracked")
    rows = c.fetchall()

    for item_id, url in rows:
        try:
            match = re.search(r'i_code=(\d+)', url)
            if not match:
                print(f"\u274c 無法解析商品 ID：{url}")
                continue
            momo_id = match.group(1)
            name, price, _ = get_momo_product_info(momo_id)

            if not price:
                print(f"❌ 無法更新商品 {item_id}")
                continue

            c.execute("UPDATE tracked SET price = ? WHERE id = ?", (price, item_id))
            c.execute("INSERT INTO price_history (product_id, price) VALUES (?, ?)", (item_id, price))
            print(f"✅ 商品 {item_id} 更新價格為 {price}")
            time.sleep(1)

        except Exception as e:
            print(f"\u274c 錯誤：{e}")

    conn.commit()
    conn.close()
    print("✅ 價格更新完成")

# 啟動排程器
scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', days=1)
scheduler.start()

# -------------------- 路由 --------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        momo_id = request.form.get('momo_id')
        name, price, url = get_momo_product_info(momo_id)

        if not name or not price:
            return "❌ 無法擷取商品資訊", 500

        insert_tracked(name, price, url)
        return redirect(url_for('index', success=1))

    items = get_all_tracked()
    success = request.args.get("success")
    return render_template('index.html', items=items, success=success)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete(product_id):
    delete_tracked(product_id)
    return redirect(url_for('index'))

@app.route('/history/<int:product_id>')
def price_history(product_id):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("SELECT name FROM tracked WHERE id = ?", (product_id,))
    name_row = c.fetchone()
    if not name_row:
        return "找不到商品", 404
    name = name_row[0]

    c.execute("SELECT price, timestamp FROM price_history WHERE product_id = ? ORDER BY timestamp", (product_id,))
    rows = c.fetchall()
    conn.close()

    prices = [r[0] for r in rows]
    timestamps = [r[1] for r in rows]

    return render_template('history.html', name=name, prices=prices, timestamps=timestamps)

# -------------------- 主程式 --------------------

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
