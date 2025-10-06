#!/usr/bin/env python3
"""
プロモーション自動掲載バッチ処理

毎日1回実行され、scheduled状態のプロモーションの中で、
開始日時を過ぎているものを自動的にactiveステータスに変更します。
"""

import sys
import os
import time
from datetime import datetime

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cloud SQL Proxyの起動を待つ
print("Cloud SQL Proxyの起動を待っています...")
time.sleep(10)
print("データベース接続を開始します...")

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import crud, models

def publish_scheduled_promotions():
    """予定されたプロモーションを公開する"""
    db: Session = SessionLocal()

    try:
        print(f"[{datetime.now()}] プロモーション自動掲載バッチ開始")

        # 公開対象のプロモーションを取得
        promotions = crud.get_scheduled_promotions_for_publishing(db)

        print(f"公開対象のプロモーション: {len(promotions)}件")

        published_count = 0
        for promotion in promotions:
            try:
                # プロモーションを公開
                published = crud.publish_promotion(db, promotion.id)
                if published:
                    print(f"  ✓ プロモーションを公開しました: ID={promotion.id}, タイトル='{promotion.title}'")
                    published_count += 1
                else:
                    print(f"  ✗ プロモーションの公開に失敗しました: ID={promotion.id}")
            except Exception as e:
                print(f"  ✗ エラー (ID={promotion.id}): {str(e)}")
                continue

        print(f"\n公開完了: {published_count}/{len(promotions)}件")
        print(f"[{datetime.now()}] プロモーション自動掲載バッチ終了\n")

        return published_count

    except Exception as e:
        print(f"エラー: {str(e)}")
        raise
    finally:
        db.close()

def expire_old_promotions():
    """期限切れのプロモーションをexpiredステータスに変更する"""
    db: Session = SessionLocal()

    try:
        print(f"[{datetime.now()}] 期限切れプロモーション処理開始")

        now = datetime.now()

        # 終了日時を過ぎたactiveプロモーションを取得
        expired_promotions = (
            db.query(models.Promotion)
            .filter(
                models.Promotion.status == "active",
                models.Promotion.end_date < now
            )
            .all()
        )

        print(f"期限切れのプロモーション: {len(expired_promotions)}件")

        expired_count = 0
        for promotion in expired_promotions:
            try:
                promotion.status = "expired"
                db.commit()
                print(f"  ✓ プロモーションを期限切れに設定しました: ID={promotion.id}, タイトル='{promotion.title}'")
                expired_count += 1
            except Exception as e:
                print(f"  ✗ エラー (ID={promotion.id}): {str(e)}")
                db.rollback()
                continue

        print(f"\n期限切れ処理完了: {expired_count}/{len(expired_promotions)}件")
        print(f"[{datetime.now()}] 期限切れプロモーション処理終了\n")

        return expired_count

    except Exception as e:
        print(f"エラー: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        # スケジュールされたプロモーションを公開
        published = publish_scheduled_promotions()

        # 期限切れプロモーションを処理
        expired = expire_old_promotions()

        print(f"=== バッチ処理完了 ===")
        print(f"公開: {published}件")
        print(f"期限切れ: {expired}件")

        sys.exit(0)

    except Exception as e:
        print(f"致命的なエラー: {str(e)}")
        sys.exit(1)
