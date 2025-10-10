#!/usr/bin/env python3
import random
import subprocess
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

def generate_and_insert_batch(batch_start, batch_end):
    """指定期間のデータを生成してデータベースに挿入"""
    sql_statements = []

    current_date = batch_start
    while current_date <= batch_end:
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
            sql_statements.append(
                f"INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at) "
                f"VALUES ({user_id}, {store_id}, '{supplier_name}', {total_amount}, '{receipt_timestamp}', NOW(), NOW());"
            )

            # レシート明細を挿入
            for item_name, item_price in selected_items:
                sql_statements.append(
                    f"INSERT INTO receipt_items (receipt_id, description, amount) "
                    f"VALUES (currval('receipts_id_seq'), '{item_name}', {item_price});"
                )

        current_date += timedelta(days=1)

    # SQLを実行
    sql_content = "\n".join(sql_statements)

    process = subprocess.Popen(
        ["psql", "-h", "localhost", "-p", "5433", "-U", "user", "-d", "dbname"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PGPASSWORD": "your-gcp-project-id-PostgreSQL16"}
    )

    stdout, stderr = process.communicate(sql_content.encode())

    if process.returncode == 0:
        print(f"✓ Batch {batch_start.date()} to {batch_end.date()} inserted successfully")
        return True
    else:
        print(f"✗ Error inserting batch {batch_start.date()} to {batch_end.date()}")
        print(stderr.decode())
        return False

# バッチサイズ: 5日ずつ
batch_size_days = 5
current_start = start_date

print("Starting batch inserts...")
while current_start <= end_date:
    current_end = min(current_start + timedelta(days=batch_size_days - 1), end_date)
    generate_and_insert_batch(current_start, current_end)
    current_start += timedelta(days=batch_size_days)

print("\nAll batches completed!")
print("\nVerifying data...")

# 最終確認
verify_process = subprocess.Popen(
    ["psql", "-h", "localhost", "-p", "5433", "-U", "user", "-d", "dbname",
     "-c", "SELECT COUNT(*) as total_receipts FROM receipts WHERE store_id = 3 AND receipt_date >= '2025-09-10' AND receipt_date <= '2025-10-11';"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env={"PGPASSWORD": "your-gcp-project-id-PostgreSQL16"}
)

stdout, stderr = verify_process.communicate()
print(stdout.decode())
