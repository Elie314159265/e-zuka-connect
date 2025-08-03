import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta

from .. import crud, schemas, models, security
from ..database import get_db
from ..gamification import BadgeEvaluationEngine, PointCalculationEngine

router = APIRouter(
    prefix="/debug",
    tags=["debug"],
)

# デバッグエンドポイントの認証を強化
def get_current_admin_user(current_user: models.User = Depends(security.get_current_user)):
    """
    デバッグエンドポイントは管理者のみアクセス可能
    """
    # 管理者チェック（is_owner=Trueまたは特定の管理者アカウント）
    if not current_user.is_owner:
        raise HTTPException(
            status_code=403,
            detail="デバッグエンドポイントへのアクセス権限がありません"
        )
    return current_user

OWNER_EMAIL = "email@example"
PRODUCT_LIST = [
    {"name": "メロンパン", "price": 180, "base_sales": 20},
    {"name": "カレーパン", "price": 220, "base_sales": 15},
    {"name": "食パン", "price": 300, "base_sales": 10},
    {"name": "クロワッサン", "price": 200, "base_sales": 18},
    {"name": "サンドイッチ", "price": 350, "base_sales": 12},
    {"name": "塩パン", "price": 150, "base_sales": 25},
]

@router.post("/generate-sample-data", status_code=201)
def generate_sample_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    指定されたオーナーのサンプルレシートデータを生���してDBに保存します。
    """
    owner = crud.get_user_by_email(db, email=OWNER_EMAIL)
    if not owner:
        raise HTTPException(status_code=404, detail=f"Owner with email {OWNER_EMAIL} not found.")

    total_receipts_created = 0
    today = datetime.utcnow().date()
    
    for i in range(7): # 過去7日分のデータを生成
        current_date = today - timedelta(days=i)
        
        # その日の天気を取得
        weather_data = crud.get_weather_data_by_date(db, current_date.strftime('%Y-%m-%d'))
        
        # 天気による客数の変動係数
        weather_factor = 1.0
        if weather_data:
            # 晴れ(0-3)なら客が増え、雨(51-99)なら減る
            if weather_data.weather_code <= 3:
                weather_factor = random.uniform(1.1, 1.3)
            elif weather_data.weather_code >= 51:
                weather_factor = random.uniform(0.6, 0.8)

        num_receipts = int(random.randint(20, 40) * weather_factor)

        for _ in range(num_receipts):
            num_items = random.randint(1, 4)
            receipt_items = []
            total_amount = 0
            
            for _ in range(num_items):
                product = random.choice(PRODUCT_LIST)
                receipt_items.append(schemas.ReceiptItemCreate(
                    description=product["name"],
                    amount=product["price"]
                ))
                total_amount += product["price"]

            receipt_data = schemas.ReceiptCreate(
                supplier_name="あさひパン店",
                total_amount=total_amount,
                receipt_date=current_date,
                items=receipt_items
            )
            crud.create_receipt(db=db, receipt=receipt_data, user_id=owner.id)
            total_receipts_created += 1

    return {"message": f"Successfully created {total_receipts_created} sample receipts for {OWNER_EMAIL}."}

@router.post("/generate-customer-receipts", status_code=201)
def generate_customer_receipts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    仮想顧客のサンプルレシートデータを生成してDBに保存します。
    """
    customers = [
        crud.get_user_by_email(db, email="customer1@example.com"),
        crud.get_user_by_email(db, email="customer2@example.com")
    ]
    owner = crud.get_user_by_email(db, email=OWNER_EMAIL)

    if not all(customers) or not owner:
        raise HTTPException(status_code=404, detail="Required customer or owner accounts not found.")

    total_receipts_created = 0
    today = datetime.utcnow().date()

    for customer in customers:
        if not customer: continue
        # 各顧客に5枚ずつレシートを生成
        for i in range(5):
            current_date = today - timedelta(days=random.randint(0, 6))
            num_items = random.randint(1, 3)
            receipt_items = []
            total_amount = 0
            
            for _ in range(num_items):
                product = random.choice(PRODUCT_LIST)
                receipt_items.append(schemas.ReceiptItemCreate(
                    description=product["name"],
                    amount=product["price"]
                ))
                total_amount += product["price"]

            receipt_data = schemas.ReceiptCreate(
                supplier_name="あさひパン店",
                total_amount=total_amount,
                receipt_date=current_date,
                items=receipt_items
            )
            # このレシートはオーナーではなく、顧客に紐づける
            crud.create_receipt(db=db, receipt=receipt_data, user_id=customer.id)
            total_receipts_created += 1
            
    return {"message": f"Successfully created {total_receipts_created} sample receipts for virtual customers."}

# ========== ゲーミフィケーション初期化デバッグ ==========

@router.post("/init-gamification")
def initialize_gamification_system(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    ゲーミフィケーション系の初期データを作成
    """
    try:
        # 1. 初期バッジを作成
        badge_engine = BadgeEvaluationEngine(db)
        badge_success = badge_engine.create_initial_badges()
        
        # 2. 初期特典を作成
        crud.create_initial_rewards(db)
        
        return {
            "message": "ゲーミフィケーション初期化完了",
            "badges_created": badge_success,
            "rewards_created": True
        }
        
    except Exception as e:
        return {
            "message": "ゲーミフィケーション初期化でエラーが発生しました",
            "error": str(e)
        }

@router.post("/test-point-calculation")
def test_point_calculation(
    user_email: str = "customer1@example.com",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    ポイント計算エンジンのテスト
    """
    try:
        user = crud.get_user_by_email(db, user_email)
        if not user:
            return {"error": f"User {user_email} not found"}
        
        # テスト用のレシートデータ
        test_receipt = {
            "supplier_name": "テスト店舗",
            "total_amount": 1500,
            "receipt_date": datetime.now()
        }
        
        test_context = {
            "upload_time": datetime.now(),
            "weather_code": 1  # 晴れ
        }
        
        point_engine = PointCalculationEngine(db)
        result = point_engine.calculate_points(test_receipt, user.id, test_context)
        
        return {
            "message": "ポイント計算テスト完了",
            "user_email": user_email,
            "total_points": result.total_points,
            "base_points": result.base_points,
            "bonus_points": result.bonus_points,
            "bonus_details": result.bonus_details
        }
        
    except Exception as e:
        return {
            "message": "ポイント計算テストでエラーが発生しました",
            "error": str(e)
        }

@router.post("/test-badge-evaluation")
def test_badge_evaluation(
    user_email: str = "customer1@example.com",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    バッジ評価エンジンのテスト
    """
    try:
        user = crud.get_user_by_email(db, user_email)
        if not user:
            return {"error": f"User {user_email} not found"}
        
        badge_engine = BadgeEvaluationEngine(db)
        awarded_badges = badge_engine.evaluate_and_award_badges(user.id)
        
        return {
            "message": "バッジ評価テスト完了",
            "user_email": user_email,
            "awarded_badges": [
                {
                    "badge_id": badge.badge_id,
                    "badge_name": badge.badge_name,
                    "is_new": badge.is_new
                } for badge in awarded_badges
            ]
        }
        
    except Exception as e:
        return {
            "message": "バッジ評価テストでエラーが発生しました",
            "error": str(e)
        }
