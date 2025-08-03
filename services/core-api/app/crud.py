from sqlalchemy.orm import Session
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

def get_weather_data_by_date(db: Session, date: str):
    return db.query(models.WeatherData).filter(models.WeatherData.date == date).first()

def get_weather_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherData).offset(skip).limit(limit).all()
