from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
from .security import get_password_hash

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        full_name=user.full_name,
        age_group=user.age_group,
        gender=user.gender,
        area=user.area,
        is_owner=user.is_owner
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 新規ユーザーのゲーミフィケーションプロファイルを作成
    if not user.is_owner:
        gamification_profile = models.GamificationProfile(user_id=db_user.id)
        db.add(gamification_profile)
        db.commit()
    
    return db_user

# Receipt CRUD
def create_receipt(db: Session, receipt: schemas.ReceiptCreate, user_id: int):
    db_receipt = models.Receipt(
        **receipt.dict(exclude={"items"}), user_id=user_id
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    
    for item_data in receipt.items:
        db_item = models.ReceiptItem(**item_data.dict(), receipt_id=db_receipt.id)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def get_receipts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Receipt).offset(skip).limit(limit).all()

# ========== ゲーミフィケーション関連CRUD ==========

def get_gamification_profile(db: Session, user_id: int):
    return db.query(models.GamificationProfile).filter(models.GamificationProfile.user_id == user_id).first()

def create_gamification_profile(db: Session, user_id: int):
    db_profile = models.GamificationProfile(user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_user_points(db: Session, user_id: int, points: int, transaction_type: str, description: str = None, metadata: dict = None):
    """
    ユーザーのポイントを更新し、トランザクション履歴を記録
    """
    profile = get_gamification_profile(db, user_id)
    if not profile:
        profile = create_gamification_profile(db, user_id)
    
    # ポイント更新
    if transaction_type == "earn":
        profile.contribution_points += points
        profile.total_earned_points += points
    elif transaction_type == "redeem":
        profile.contribution_points -= points
    
    # トランザクション記録
    transaction = models.PointTransaction(
        profile_id=profile.id,
        transaction_type=transaction_type,
        points=points if transaction_type == "earn" else -points,
        description=description,
        transaction_metadata=metadata
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(profile)
    
    return profile

def create_badge(db: Session, badge: schemas.BadgeCreate):
    db_badge = models.Badge(**badge.dict())
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    return db_badge

def award_badge(db: Session, user_id: int, badge_id: int):
    """
    ユーザーにバッジを授与
    """
    profile = get_gamification_profile(db, user_id)
    if not profile:
        profile = create_gamification_profile(db, user_id)
    
    # 既に持っているかチェック
    existing = db.query(models.UserBadge).filter(
        models.UserBadge.profile_id == profile.id,
        models.UserBadge.badge_id == badge_id
    ).first()
    
    if existing:
        return existing
    
    user_badge = models.UserBadge(
        profile_id=profile.id,
        badge_id=badge_id
    )
    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)
    
    return user_badge

def get_user_badges(db: Session, user_id: int):
    profile = get_gamification_profile(db, user_id)
    if not profile:
        return []
    
    return db.query(models.UserBadge).filter(
        models.UserBadge.profile_id == profile.id
    ).all()

# ========== LINE連携CRUD ==========

def create_line_integration(db: Session, line_integration: schemas.LineIntegrationCreate):
    db_integration = models.LineIntegration(**line_integration.dict())
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    return db_integration

def get_line_integration_by_user(db: Session, user_id: int):
    return db.query(models.LineIntegration).filter(
        models.LineIntegration.user_id == user_id
    ).first()

def get_line_integration_by_line_id(db: Session, line_user_id: str):
    return db.query(models.LineIntegration).filter(
        models.LineIntegration.line_user_id == line_user_id
    ).first()

# ========== 事業者関連CRUD ==========

def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_store(db: Session, store_id: int):
    return db.query(models.Store).filter(models.Store.id == store_id).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).filter(models.Store.is_active == True).offset(skip).limit(limit).all()

def create_store_owner(db: Session, store_owner: schemas.StoreOwnerCreate):
    hashed_password = get_password_hash(store_owner.password)
    db_owner = models.StoreOwner(
        **store_owner.dict(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

def get_store_owner_by_email(db: Session, email: str):
    return db.query(models.StoreOwner).filter(models.StoreOwner.email == email).first()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_store_events(db: Session, store_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(
        models.Event.store_id == store_id,
        models.Event.is_active == True
    ).offset(skip).limit(limit).all()

def get_public_events(db: Session, skip: int = 0, limit: int = 100):
    """公開イベント一覧（一般ユーザー向け）"""
    return db.query(models.Event).filter(
        models.Event.is_active == True
    ).offset(skip).limit(limit).all()

def create_archive_content(db: Session, content: schemas.ArchiveContentCreate):
    db_content = models.ArchiveContent(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_store_archive_contents(db: Session, store_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ArchiveContent).filter(
        models.ArchiveContent.store_id == store_id
    ).offset(skip).limit(limit).all()

def get_public_archive_contents(db: Session, skip: int = 0, limit: int = 100):
    """公開アーカイブコンテンツ一覧（一般ユーザー向け）"""
    return db.query(models.ArchiveContent).filter(
        models.ArchiveContent.is_published == True
    ).offset(skip).limit(limit).all()

# ========== 特典・報酬システムCRUD ==========

import secrets
import string
from datetime import datetime, timedelta

def get_rewards(db: Session, skip: int = 0, limit: int = 100, is_active: bool = True):
    """特典一覧を取得"""
    query = db.query(models.Reward)
    if is_active:
        query = query.filter(models.Reward.is_active == True)
    return query.offset(skip).limit(limit).all()

def get_reward(db: Session, reward_id: int):
    """特定の特典を取得"""
    return db.query(models.Reward).filter(models.Reward.id == reward_id).first()

def create_reward(db: Session, reward: schemas.RewardCreate):
    """特典を作成"""
    db_reward = models.Reward(
        **reward.dict(),
        available_stock=reward.stock_quantity
    )
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

def generate_coupon_code(reward_id: int, user_id: int) -> str:
    """
    クーポンコードを生成
    フォーマット: EZ-{REWARD_TYPE}-{6桁ランダム}
    """
    # 6桁のランダム文字列を生成
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    # 簡易的な報酬タイプ識別
    reward_type = "GEN"  # General
    
    return f"EZ-{reward_type}-{random_part}"

def redeem_reward(db: Session, user_id: int, reward_id: int):
    """
    特典を交換する
    """
    # 特典の存在と有効性を確認
    reward = get_reward(db, reward_id)
    if not reward or not reward.is_active:
        raise ValueError("特典が見つからないか、無効です")
    
    # 在庫確認
    if reward.stock_quantity is not None and (reward.available_stock or 0) <= 0:
        raise ValueError("特典の在庫が不足しています")
    
    # ユーザーのポイント残高確認
    profile = get_gamification_profile(db, user_id)
    if not profile or profile.contribution_points < reward.required_points:
        raise ValueError("ポイントが不足しています")
    
    # クーポンコード生成
    coupon_code = generate_coupon_code(reward_id, user_id)
    
    # 有効期限計算
    expires_at = datetime.now() + timedelta(days=reward.valid_days)
    
    # ユーザー特典交換記録作成
    user_reward = models.UserReward(
        user_id=user_id,
        reward_id=reward_id,
        coupon_code=coupon_code,
        redeemed_points=reward.required_points,
        expires_at=expires_at
    )
    db.add(user_reward)
    
    # ポイント消費
    update_user_points(
        db,
        user_id,
        reward.required_points,
        "redeem",
        f"特典交換: {reward.title}",
        {"reward_id": reward_id, "coupon_code": coupon_code}
    )
    
    # 在庫更新
    if reward.stock_quantity is not None:
        reward.available_stock = (reward.available_stock or 0) - 1
    
    db.commit()
    db.refresh(user_reward)
    
    return user_reward

def get_user_rewards(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """ユーザーの特典交換履歴を取得"""
    return db.query(models.UserReward).filter(
        models.UserReward.user_id == user_id
    ).order_by(models.UserReward.created_at.desc()).offset(skip).limit(limit).all()

def get_user_reward_by_coupon(db: Session, coupon_code: str):
    """クーポンコードで特典を取得"""
    return db.query(models.UserReward).filter(
        models.UserReward.coupon_code == coupon_code
    ).first()

def use_coupon(db: Session, coupon_code: str, store_id: int = None):
    """クーポンを使用する"""
    user_reward = get_user_reward_by_coupon(db, coupon_code)
    
    if not user_reward:
        raise ValueError("クーポンが見つかりません")
    
    if user_reward.status != "active":
        raise ValueError("クーポンは既に使用済みまたは期限切れです")
    
    if user_reward.expires_at and user_reward.expires_at < datetime.now():
        user_reward.status = "expired"
        db.commit()
        raise ValueError("クーポンの有効期限が切れています")
    
    # クーポン使用記録
    user_reward.status = "used"
    user_reward.used_at = datetime.now()
    if store_id:
        user_reward.used_store_id = store_id
    
    db.commit()
    db.refresh(user_reward)
    
    return user_reward

def create_initial_rewards(db: Session):
    """初期特典データを作成"""
    initial_rewards = [
        {
            "title": "100円割引券",
            "description": "全加盟店で使える100円割引クーポン",
            "required_points": 500,
            "reward_type": "coupon",
            "valid_days": 30,
            "terms_conditions": "500円以上のお買い物でご利用いただけます",
            "is_featured": True
        },
        {
            "title": "コロッケ1個プレゼント",
            "description": "商店街の人気コロッケ屋さんで使えるコロッケ券",
            "required_points": 800,
            "reward_type": "gift",
            "valid_days": 14,
            "stock_quantity": 50,
            "available_stock": 50
        },
        {
            "title": "シークレット特典",
            "description": "毎月変わる特別な特典。今月は何が出るかお楽しみ！",
            "required_points": 1500,
            "reward_type": "experience",
            "valid_days": 7,
            "stock_quantity": 10,
            "available_stock": 10,
            "is_featured": True
        }
    ]
    
    for reward_data in initial_rewards:
        existing = db.query(models.Reward).filter(
            models.Reward.title == reward_data["title"]
        ).first()
        
        if not existing:
            reward = models.Reward(**reward_data)
            db.add(reward)
    
    db.commit()

# WeatherData CRUD
def create_weather_data(db: Session, weather: schemas.WeatherDataCreate):
    db_weather = models.WeatherData(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def upsert_weather_data(db: Session, weather: schemas.WeatherDataCreate):
    """
    天気データをUPSERT（更新または作成）する
    同じ日付のデータが存在する場合は更新、存在しない場合は新規作成
    """
    from datetime import datetime

    # 日付を正規化（date型をdatetime型に変換）
    target_date = weather.date
    if hasattr(target_date, 'date'):
        target_date = target_date.date()
    target_datetime = datetime.combine(target_date, datetime.min.time())

    # 既存データを検索
    existing = db.query(models.WeatherData).filter(
        models.WeatherData.date == target_datetime
    ).first()

    if existing:
        # 既存データを更新
        for key, value in weather.dict().items():
            if value is not None:  # Noneでない値のみ更新
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 新規作成
        weather_dict = weather.dict()
        weather_dict['date'] = target_datetime
        db_weather = models.WeatherData(**weather_dict)
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
        return db_weather

def get_weather_data_by_date(db: Session, date: str):
    return db.query(models.WeatherData).filter(models.WeatherData.date == date).first()

def get_weather_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherData).offset(skip).limit(limit).all()

def get_weather_data_in_date_range(db: Session, start_date, end_date):
    """
    指定した日付範囲の天気データを取得する
    Args:
        start_date: 開始日
        end_date: 終了日
    """
    from datetime import datetime

    # date型をdatetime型に変換
    start_datetime = datetime.combine(start_date, datetime.min.time()) if hasattr(start_date, 'day') else start_date
    end_datetime = datetime.combine(end_date, datetime.max.time()) if hasattr(end_date, 'day') else end_date

    return db.query(models.WeatherData).filter(
        models.WeatherData.date >= start_datetime,
        models.WeatherData.date <= end_datetime
    ).order_by(models.WeatherData.date).all()

def delete_old_weather_data(db: Session, days_to_keep: int = 7):
    """
    指定した日数より古い天気データを削除する
    Args:
        days_to_keep: 保持する日数（デフォルト7日）
    """
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = db.query(models.WeatherData).filter(
        models.WeatherData.date < cutoff_date
    ).delete()
    db.commit()
    return deleted_count

def delete_weather_data_in_range(db: Session, start_date, end_date):
    """
    指定した日付範囲の天気データを削除する（洗い替え用）
    Args:
        start_date: 削除開始日
        end_date: 削除終了日
    """
    from datetime import datetime

    # date型をdatetime型に変換
    start_datetime = datetime.combine(start_date, datetime.min.time()) if hasattr(start_date, 'day') else start_date
    end_datetime = datetime.combine(end_date, datetime.max.time()) if hasattr(end_date, 'day') else end_date

    deleted_count = db.query(models.WeatherData).filter(
        models.WeatherData.date >= start_datetime,
        models.WeatherData.date <= end_datetime
    ).delete()
    db.commit()
    return deleted_count

def delete_future_weather_data(db: Session, from_date):
    """
    指定した日付以降の天気データを削除する（予報データ更新用）
    Args:
        from_date: この日付以降のデータを削除
    """
    from datetime import datetime

    # date型をdatetime型に変換
    from_datetime = datetime.combine(from_date, datetime.min.time()) if hasattr(from_date, 'day') else from_date

    deleted_count = db.query(models.WeatherData).filter(
        models.WeatherData.date >= from_datetime
    ).delete()
    db.commit()
    return deleted_count

# Historical WeatherData CRUD
def create_historical_weather_data(db: Session, weather: schemas.HistoricalWeatherDataCreate):
    """過去気象データを作成"""
    db_weather = models.HistoricalWeatherData(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def get_historical_weather_data_by_date(db: Session, date: str):
    """指定日付の過去気象データを取得"""
    return db.query(models.HistoricalWeatherData).filter(models.HistoricalWeatherData.date == date).first()

def get_historical_weather_data(db: Session, skip: int = 0, limit: int = 100):
    """過去気象データ一覧を取得"""
    return db.query(models.HistoricalWeatherData).order_by(models.HistoricalWeatherData.date.desc()).offset(skip).limit(limit).all()

def get_historical_weather_data_in_date_range(db: Session, start_date, end_date):
    """指定日付範囲の過去気象データを取得"""
    from datetime import datetime

    # date型をdatetime型に変換
    start_datetime = datetime.combine(start_date, datetime.min.time()) if hasattr(start_date, 'day') else start_date
    end_datetime = datetime.combine(end_date, datetime.max.time()) if hasattr(end_date, 'day') else end_date

    return db.query(models.HistoricalWeatherData).filter(
        models.HistoricalWeatherData.date >= start_datetime,
        models.HistoricalWeatherData.date <= end_datetime
    ).order_by(models.HistoricalWeatherData.date).all()

def delete_historical_weather_data_in_range(db: Session, start_date, end_date):
    """指定日付範囲の過去気象データを削除"""
    from datetime import datetime

    start_datetime = datetime.combine(start_date, datetime.min.time()) if hasattr(start_date, 'day') else start_date
    end_datetime = datetime.combine(end_date, datetime.max.time()) if hasattr(end_date, 'day') else end_date

    deleted_count = db.query(models.HistoricalWeatherData).filter(
        models.HistoricalWeatherData.date >= start_datetime,
        models.HistoricalWeatherData.date <= end_datetime
    ).delete()
    db.commit()
    return deleted_count

def upsert_historical_weather_data(db: Session, weather: schemas.HistoricalWeatherDataCreate):
    """
    過去気象データを挿入または更新（UPSERT）
    同じ日付のデータが存在する場合は更新、なければ新規作成
    """
    existing = get_historical_weather_data_by_date(db, weather.date.strftime('%Y-%m-%d %H:%M:%S%z'))

    if existing:
        # 更新
        for key, value in weather.dict(exclude={'date'}).items():
            if value is not None:  # None以外の値のみ更新
                setattr(existing, key, value)

        from datetime import datetime
        existing.updated_at = datetime.now()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 新規作成
        return create_historical_weather_data(db, weather)

# ========== 商品管理 CRUD ==========

# ProductCategory CRUD
def create_product_category(db: Session, category: schemas.ProductCategoryCreate):
    """商品カテゴリを作成"""
    db_category = models.ProductCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_product_categories(db: Session, store_id: int, skip: int = 0, limit: int = 100):
    """店舗の商品カテゴリ一覧を取得"""
    return db.query(models.ProductCategory).filter(
        models.ProductCategory.store_id == store_id
    ).order_by(models.ProductCategory.sort_order, models.ProductCategory.name).offset(skip).limit(limit).all()

def get_product_category(db: Session, category_id: int):
    """商品カテゴリを取得"""
    return db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()

def update_product_category(db: Session, category_id: int, category_update: schemas.ProductCategoryUpdate):
    """商品カテゴリを更新"""
    db_category = get_product_category(db, category_id)
    if not db_category:
        return None

    update_data = category_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    from datetime import datetime
    db_category.updated_at = datetime.now()
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_product_category(db: Session, category_id: int):
    """商品カテゴリを削除"""
    db_category = get_product_category(db, category_id)
    if not db_category:
        return False

    db.delete(db_category)
    db.commit()
    return True

# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate):
    """商品を作成"""
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, store_id: int, category_id: int = None, is_active: bool = None,
                skip: int = 0, limit: int = 100):
    """店舗の商品一覧を取得"""
    query = db.query(models.Product).filter(models.Product.store_id == store_id)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    if is_active is not None:
        query = query.filter(models.Product.is_active == is_active)

    return query.order_by(models.Product.name).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    """商品を取得"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_code(db: Session, store_id: int, product_code: str):
    """商品コードで商品を取得"""
    return db.query(models.Product).filter(
        models.Product.store_id == store_id,
        models.Product.product_code == product_code
    ).first()

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    """商品を更新"""
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    from datetime import datetime
    db_product.updated_at = datetime.now()
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """商品を削除"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True

def update_product_stock(db: Session, product_id: int, quantity_change: int, reason: str = "adjustment"):
    """商品在庫を更新"""
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    if not db_product.is_stock_managed:
        return db_product  # 在庫管理対象外の場合はそのまま返す

    new_stock = db_product.stock_quantity + quantity_change
    if new_stock < 0:
        raise ValueError("在庫数が負の値になります")

    db_product.stock_quantity = new_stock

    from datetime import datetime
    db_product.updated_at = datetime.now()
    db.commit()
    db.refresh(db_product)
    return db_product

def get_low_stock_products(db: Session, store_id: int):
    """在庫が少ない商品を取得"""
    return db.query(models.Product).filter(
        models.Product.store_id == store_id,
        models.Product.is_stock_managed == True,
        models.Product.is_active == True,
        models.Product.stock_quantity <= models.Product.low_stock_threshold
    ).order_by(models.Product.stock_quantity).all()

def search_products(db: Session, store_id: int, search_query: str, skip: int = 0, limit: int = 100):
    """商品を検索"""
    search_term = f"%{search_query}%"
    return db.query(models.Product).filter(
        models.Product.store_id == store_id,
        models.Product.is_active == True,
        (models.Product.name.ilike(search_term) |
         models.Product.description.ilike(search_term) |
         models.Product.product_code.ilike(search_term))
    ).order_by(models.Product.name).offset(skip).limit(limit).all()

def get_featured_products(db: Session, store_id: int, limit: int = 10):
    """おすすめ商品を取得"""
    return db.query(models.Product).filter(
        models.Product.store_id == store_id,
        models.Product.is_active == True,
        models.Product.is_featured == True
    ).order_by(models.Product.name).limit(limit).all()

def get_seasonal_products(db: Session, store_id: int, limit: int = 10):
    """季節商品を取得"""
    return db.query(models.Product).filter(
        models.Product.store_id == store_id,
        models.Product.is_active == True,
        models.Product.is_seasonal == True
    ).order_by(models.Product.name).limit(limit).all()

# ========== 店舗マッチングロジック ==========

def normalize_phone_number(phone: str) -> str:
    """
    電話番号を正規化（ハイフン、スペース、括弧を削除）
    例: 092-123-4567 -> 0921234567
    """
    if not phone:
        return ""
    import re
    return re.sub(r'[\s\-\(\)]', '', phone)

def find_or_create_store(db: Session, supplier_name: str, supplier_phone: str = None):
    """
    OCRで抽出した店名と電話番号から店舗を検索またはマッチング
    1. 電話番号が一致する店舗を優先検索
    2. 店名の部分一致で検索
    3. 見つからなければ新規店舗を自動作成

    Args:
        supplier_name: OCRで抽出した店名
        supplier_phone: OCRで抽出した電話番号（オプション）

    Returns:
        Store: マッチングまたは作成された店舗
    """
    # 1. 電話番号での検索（最優先）
    if supplier_phone:
        normalized_phone = normalize_phone_number(supplier_phone)
        if normalized_phone:
            # 電話番号の正規化一致検索
            stores = db.query(models.Store).filter(
                models.Store.phone.isnot(None)
            ).all()

            for store in stores:
                if normalize_phone_number(store.phone) == normalized_phone:
                    return store

    # 2. 店名での部分一致検索
    if supplier_name:
        store = db.query(models.Store).filter(
            models.Store.name.ilike(f"%{supplier_name}%")
        ).first()

        if store:
            return store

        # 逆パターン: DBの店名がOCR店名に含まれるか
        stores = db.query(models.Store).all()
        for store in stores:
            if store.name and store.name in supplier_name:
                return store

    # 3. 見つからない場合は新規店舗を自動作成
    new_store = models.Store(
        name=supplier_name or "不明な店舗",
        phone=supplier_phone,
        business_type="未分類",
        is_active=True
    )
    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    return new_store

# ========== Promotion CRUD ==========

def create_promotion(db: Session, promotion: schemas.PromotionCreate):
    """プロモーションを作成"""
    db_promotion = models.Promotion(**promotion.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def get_promotion(db: Session, promotion_id: int):
    """プロモーションを取得"""
    return db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()

def get_promotions(
    db: Session,
    store_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """プロモーション一覧を取得"""
    query = db.query(models.Promotion).filter(models.Promotion.store_id == store_id)

    if status:
        query = query.filter(models.Promotion.status == status)

    return query.order_by(models.Promotion.display_priority.desc(), models.Promotion.created_at.desc()).offset(skip).limit(limit).all()

def get_active_promotions(db: Session, limit: int = 10):
    """アクティブなプロモーション一覧を取得（ユーザー向け）"""
    from datetime import datetime
    now = datetime.now()

    return (
        db.query(models.Promotion)
        .filter(
            models.Promotion.status == "active",
            models.Promotion.start_date <= now,
            models.Promotion.end_date >= now
        )
        .order_by(models.Promotion.display_priority.desc(), models.Promotion.created_at.desc())
        .limit(limit)
        .all()
    )

def update_promotion(db: Session, promotion_id: int, promotion_update: schemas.PromotionUpdate):
    """プロモーションを更新"""
    db_promotion = get_promotion(db, promotion_id)
    if not db_promotion:
        return None

    update_data = promotion_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_promotion, field, value)

    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def delete_promotion(db: Session, promotion_id: int):
    """プロモーションを削除"""
    db_promotion = get_promotion(db, promotion_id)
    if not db_promotion:
        return False

    db.delete(db_promotion)
    db.commit()
    return True

def increment_promotion_views(db: Session, promotion_id: int):
    """プロモーションの閲覧数を増やす"""
    db_promotion = get_promotion(db, promotion_id)
    if not db_promotion:
        return None

    db_promotion.current_views += 1
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def get_scheduled_promotions_for_publishing(db: Session):
    """自動掲載対象のプロモーションを取得（バッチ処理用）"""
    from datetime import datetime
    now = datetime.now()

    return (
        db.query(models.Promotion)
        .filter(
            models.Promotion.status == "scheduled",
            models.Promotion.is_auto_published == True,
            models.Promotion.start_date <= now,
            models.Promotion.end_date >= now
        )
        .all()
    )

def publish_promotion(db: Session, promotion_id: int):
    """プロモーションを公開状態にする"""
    from datetime import datetime

    db_promotion = get_promotion(db, promotion_id)
    if not db_promotion:
        return None

    db_promotion.status = "active"
    db_promotion.published_at = datetime.now()

    db.commit()
    db.refresh(db_promotion)
    return db_promotion
