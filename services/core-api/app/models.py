from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    age_group = Column(String, index=True)  # e.g., "20s", "30s", "40s"
    gender = Column(String)  # e.g., "male", "female", "other"
    area = Column(String, index=True)  # 居住エリア
    is_owner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    receipts = relationship("Receipt", back_populates="user")
    gamification_profile = relationship("GamificationProfile", back_populates="user", uselist=False)
    line_integration = relationship("LineIntegration", back_populates="user", uselist=False)
    user_rewards = relationship("UserReward", back_populates="user")

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)  # マルチテナンシー用
    supplier_name = Column(String, index=True)
    total_amount = Column(Integer)
    receipt_date = Column(DateTime(timezone=True), server_default=func.now())
    image_gcs_path = Column(String)  # GCS画像パス
    ocr_raw_data = Column(JSON)  # Document AI生データ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションシップ
    user = relationship("User", back_populates="receipts")
    store = relationship("Store", back_populates="receipts")
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")

class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    description = Column(String)
    amount = Column(Integer)

    receipt = relationship("Receipt", back_populates="items")

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), unique=True, index=True)
    temperature_max = Column(Float)  # 最高気温
    temperature_min = Column(Float)  # 最低気温
    humidity = Column(Float)
    weather_code = Column(Integer) # WMO Weather interpretation codes

# ========== 過去気象データ分析用テーブル ==========

class HistoricalWeatherData(Base):
    __tablename__ = "historical_weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), unique=True, index=True)

    # 基本気温データ
    temperature_max = Column(Float)  # 最高気温 (°C)
    temperature_min = Column(Float)  # 最低気温 (°C)
    temperature_mean = Column(Float)  # 平均気温 (°C)

    # 降水データ
    precipitation_sum = Column(Float)  # 総降水量 (mm)
    rain_sum = Column(Float)  # 雨量 (mm)
    snowfall_sum = Column(Float)  # 降雪量 (cm)

    # 湿度・風データ
    humidity_mean = Column(Float)  # 平均湿度 (%)
    wind_speed_max = Column(Float)  # 最大風速 (km/h)
    wind_direction = Column(Integer)  # 風向 (度)

    # 気圧・日照
    pressure_mean = Column(Float)  # 平均気圧 (hPa)
    sunshine_duration = Column(Float)  # 日照時間 (hours)

    # データソース情報
    data_source = Column(String, default="open-meteo")  # データソース
    weather_code = Column(Integer)  # WMO Weather interpretation codes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# ========== 顧客向けゲーミフィケーション関連テーブル ==========

class GamificationProfile(Base):
    __tablename__ = "gamification_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    contribution_points = Column(Integer, default=0)  # 現在の貢献ポイント(CP)
    total_earned_points = Column(Integer, default=0)  # 累計獲得ポイント
    level = Column(Integer, default=1)  # ユーザーレベル
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    user = relationship("User", back_populates="gamification_profile")
    badges = relationship("UserBadge", back_populates="profile")
    point_transactions = relationship("PointTransaction", back_populates="profile")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon_url = Column(String)  # バッジアイコンのURL
    criteria = Column(JSON)  # 獲得条件（JSON形式）
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("gamification_profiles.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    profile = relationship("GamificationProfile", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")

class PointTransaction(Base):
    __tablename__ = "point_transactions"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("gamification_profiles.id"), nullable=False)
    transaction_type = Column(String, nullable=False)  # "earn", "redeem", "exchange"
    points = Column(Integer, nullable=False)  # 正の値=獲得、負の値=消費
    description = Column(String)
    transaction_metadata = Column(JSON)  # 追加情報（レシートID、イベントIDなど）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    profile = relationship("GamificationProfile", back_populates="point_transactions")

# ========== LINE連携テーブル ==========

class LineIntegration(Base):
    __tablename__ = "line_integrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    line_user_id = Column(String, unique=True, nullable=False)  # LINE User ID
    line_display_name = Column(String)
    is_active = Column(Boolean, default=True)
    linked_at = Column(DateTime(timezone=True), server_default=func.now())
    last_message_at = Column(DateTime(timezone=True))
    
    # リレーションシップ
    user = relationship("User", back_populates="line_integration")

# ========== 事業者向けテーブル ==========

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    business_type = Column(String, index=True)  # 業種
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    owners = relationship("StoreOwner", back_populates="store")
    events = relationship("Event", back_populates="store")
    receipts = relationship("Receipt", back_populates="store")
    archive_contents = relationship("ArchiveContent", back_populates="store")
    rewards = relationship("Reward", back_populates="store")
    product_categories = relationship("ProductCategory", back_populates="store")
    products = relationship("Product", back_populates="store")
    promotions = relationship("Promotion", back_populates="store")

class StoreOwner(Base):
    __tablename__ = "store_owners"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="owner")  # "owner", "manager", "staff"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # リレーションシップ
    store = relationship("Store", back_populates="owners")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)  # マルチテナンシー
    title = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(String, index=True)  # "sale", "event", "coupon"
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    discount_rate = Column(Float)  # 割引率（%）
    coupon_code = Column(String, unique=True)
    target_products = Column(JSON)  # 対象商品リスト
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    store = relationship("Store", back_populates="events")

class ArchiveContent(Base):
    __tablename__ = "archive_contents"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)  # マルチテナンシー
    title = Column(String, nullable=False)
    content = Column(Text)
    content_type = Column(String, index=True)  # "story", "history", "photo"
    image_urls = Column(JSON)  # 画像URLのリスト
    tags = Column(JSON)  # タグのリスト
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    store = relationship("Store", back_populates="archive_contents")

# ========== 特典・報酬システムテーブル ==========

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    required_points = Column(Integer, nullable=False)
    reward_type = Column(String, nullable=False)  # 'coupon', 'gift', 'experience', 'digital'
    store_id = Column(Integer, ForeignKey("stores.id"))  # NULL = 全店共通
    stock_quantity = Column(Integer)  # NULL = 無制限
    available_stock = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    valid_days = Column(Integer, default=30)  # クーポン有効日数
    terms_conditions = Column(Text)
    image_url = Column(String)
    expires_at = Column(DateTime(timezone=True))  # 特典自体の期限
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    store = relationship("Store", back_populates="rewards")
    user_rewards = relationship("UserReward", back_populates="reward")

class UserReward(Base):
    __tablename__ = "user_rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("rewards.id"), nullable=False)
    coupon_code = Column(String, unique=True)  # 生成されたクーポンコード
    redeemed_points = Column(Integer, nullable=False)
    status = Column(String, default="active")  # 'active', 'used', 'expired'
    expires_at = Column(DateTime(timezone=True))  # 個別クーポンの期限
    used_at = Column(DateTime(timezone=True))
    used_store_id = Column(Integer, ForeignKey("stores.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    user = relationship("User", back_populates="user_rewards")
    reward = relationship("Reward", back_populates="user_rewards")
    used_store = relationship("Store", foreign_keys=[used_store_id])

# ========== 商品管理テーブル ==========

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    parent_category_id = Column(Integer, ForeignKey("product_categories.id"))  # 階層構造
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)  # 表示順序
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションシップ
    store = relationship("Store", back_populates="product_categories")
    parent = relationship("ProductCategory", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    product_code = Column(String, index=True)  # 商品コード（JANコード等）
    unit_price = Column(Integer, nullable=False)  # 単価（円単位）
    cost_price = Column(Integer)  # 原価（円単位）
    tax_rate = Column(Float, default=0.10)  # 消費税率
    unit = Column(String, default="個")  # 単位（個、kg、L等）

    # 在庫管理
    stock_quantity = Column(Integer, default=0)  # 在庫数
    low_stock_threshold = Column(Integer, default=10)  # 在庫少警告閾値
    is_stock_managed = Column(Boolean, default=True)  # 在庫管理対象か

    # 商品状態
    is_active = Column(Boolean, default=True)  # 販売中かどうか
    is_featured = Column(Boolean, default=False)  # おすすめ商品か
    is_seasonal = Column(Boolean, default=False)  # 季節商品か

    # 販売情報
    sale_start_date = Column(DateTime(timezone=True))  # 販売開始日
    sale_end_date = Column(DateTime(timezone=True))    # 販売終了日

    # 画像・メディア
    image_urls = Column(JSON)  # 商品画像URLのリスト

    # メタデータ
    tags = Column(JSON)  # タグのリスト
    allergen_info = Column(JSON)  # アレルギー情報
    nutritional_info = Column(JSON)  # 栄養成分情報

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションシップ
    store = relationship("Store", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")
    promotions = relationship("Promotion", back_populates="product")

# ========== プロモーション管理テーブル ==========

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # プロモーション内容
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    promotion_text = Column(Text)  # 事業者が入力するプロモーション文章

    # 画像・メディア
    promotion_image_urls = Column(JSON)  # プロモーション用画像URLのリスト

    # スケジュール
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # 掲載ステータス
    status = Column(String, default="draft", index=True)  # "draft", "scheduled", "active", "expired", "paused"
    is_auto_published = Column(Boolean, default=True)  # 自動掲載するか
    published_at = Column(DateTime(timezone=True))  # 実際に掲載された日時

    # プロモーション設定
    display_priority = Column(Integer, default=0)  # 表示優先度（高い数値ほど優先）
    target_audience = Column(JSON)  # ターゲット層（年齢層、性別など）
    max_views = Column(Integer)  # 最大表示回数（NULL=無制限）
    current_views = Column(Integer, default=0)  # 現在の表示回数

    # メタデータ
    tags = Column(JSON)  # タグのリスト

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションシップ
    store = relationship("Store", back_populates="promotions")
    product = relationship("Product", back_populates="promotions")

# ========== 初期バッジデータ定義 ==========

class InitialBadgeData(Base):
    """初期バッジデータを定義するための一時テーブル"""
    __tablename__ = "initial_badge_data"

    id = Column(Integer, primary_key=True, index=True)
    processed = Column(Boolean, default=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
