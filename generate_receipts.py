#!/usr/bin/env python3
import random
from datetime import datetime, timedelta

# パン商品のリスト
bread_items = [
    ('クロワッサン', 200), ('メロンパン', 180), ('あんぱん', 150), ('カレーパン', 220),
    ('クリームパン', 180), ('フランスパン', 320), ('ロールパン', 140), ('チョコパン', 170),
    ('ベーグル', 230), ('デニッシュ', 210), ('バゲット', 280), ('食パン', 300),
    ('コロッケパン', 200), ('ソーセージパン', 190), ('チーズパン', 180), ('塩パン', 160),
    ('よもぎあんぱん', 170), ('クリームコロネ', 190), ('ツナマヨパン', 200), ('ピザパン', 250),
    ('焼きそばパン', 230), ('たまごサンド', 280), ('ハムサンド', 320), ('ツナサンド', 290),
    ('シナモンロール', 240), ('アップルパイ', 260), ('チョコクロワッサン', 250), ('くるみパン', 190),
]

user_ids = [1, 2, 3]
store_id = 3
supplier_name = "パン工房"

# 期間の設定
start_date = datetime(2025, 9, 10)
end_date = datetime(2025, 10, 11)

receipt_id = 1000  # 大きな番号から始めて既存データと重複しないように

print("BEGIN;")
print()

current_date = start_date
while current_date <= end_date:
    # 1日あたり5-8件のレシートを生成
    receipts_per_day = random.randint(5, 8)

    for _ in range(receipts_per_day):
        # ランダムなユーザー
        user_id = random.choice(user_ids)

        # ランダムな時刻（9:00-19:00）
        hour = random.randint(9, 19)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        receipt_timestamp = current_date.replace(hour=hour, minute=minute, second=second)

        # レシート明細の件数（2-6個のパン）
        item_count = random.randint(2, 6)

        # ランダムなパンを選択
        selected_items = random.choices(bread_items, k=item_count)
        total_amount = sum(price for _, price in selected_items)

        # レシートを挿入
        print(f"INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)")
        print(f"VALUES ({user_id}, {store_id}, '{supplier_name}', {total_amount}, '{receipt_timestamp}', NOW(), NOW());")
        print()

        # レシート明細を挿入
        for item_name, item_price in selected_items:
            print(f"INSERT INTO receipt_items (receipt_id, description, amount)")
            print(f"VALUES (currval('receipts_id_seq'), '{item_name}', {item_price});")
            print()

        receipt_id += 1

    current_date += timedelta(days=1)

print("COMMIT;")
print()
print("-- 挿入されたデータの確認")
print("SELECT COUNT(*) as total_receipts FROM receipts WHERE store_id = 3 AND receipt_date >= '2025-09-10' AND receipt_date <= '2025-10-11';")
print("SELECT MIN(receipt_date) as earliest, MAX(receipt_date) as latest FROM receipts WHERE store_id = 3 AND receipt_date >= '2025-09-10' AND receipt_date <= '2025-10-11';")
