import sqlite3

conn = sqlite3.connect('tracker.db')
c = conn.cursor()

print("📌 tracked（追蹤商品）")
for row in c.execute("SELECT id, name, price, url FROM tracked"):
    print(row)

print("\n📈 price_history（價格歷史）")
for row in c.execute("SELECT product_id, price, timestamp FROM price_history ORDER BY timestamp"):
    print(row)

conn.close()