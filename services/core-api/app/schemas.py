from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# WeatherData Schemas
class WeatherDataBase(BaseModel):
    date: datetime
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None
    humidity: Optional[float] = None
    weather_code: int

class WeatherDataCreate(WeatherDataBase):
    pass

class WeatherData(WeatherDataBase):
    id: int

    class Config:
        from_attributes = True

# Historical Weather Data Schemas
class HistoricalWeatherDataBase(BaseModel):
    date: datetime
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None
    temperature_mean: Optional[float] = None
    precipitation_sum: Optional[float] = None
    rain_sum: Optional[float] = None
    snowfall_sum: Optional[float] = None
    humidity_mean: Optional[float] = None
    wind_speed_max: Optional[float] = None
    wind_direction: Optional[int] = None
    pressure_mean: Optional[float] = None
    sunshine_duration: Optional[float] = None
    data_source: str = "open-meteo"
    weather_code: Optional[int] = None

class HistoricalWeatherDataCreate(HistoricalWeatherDataBase):
    pass

class HistoricalWeatherData(HistoricalWeatherDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ReceiptItem Schemas
class ReceiptItemBase(BaseModel):
    description: Optional[str] = None
    amount: Optional[int] = None

class ReceiptItemCreate(ReceiptItemBase):
    pass

class ReceiptItem(ReceiptItemBase):
    id: int
    receipt_id: int

    class Config:
        from_attributes = True

# Receipt Schemas
class ReceiptBase(BaseModel):
    supplier_name: Optional[str] = None
    total_amount: Optional[int] = None
    receipt_date: Optional[datetime] = None
    store_id: Optional[int] = None
    image_gcs_path: Optional[str] = None
    ocr_raw_data: Optional[Dict[str, Any]] = None

class ReceiptCreate(ReceiptBase):
    items: List[ReceiptItemCreate] = []

class Receipt(ReceiptBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List[ReceiptItem] = []

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    area: Optional[str] = None
    is_owner: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    receipts: List[Receipt] = []

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    email: Optional[str] = None
    store_id: Optional[int] = None  # 事業者認証用

# Analysis Schemas
class SalesByWeatherResponse(BaseModel):
    sunny_days_sales: float
    rainy_days_sales: float
    sunny_days_count: int
    rainy_days_count: int

class DailySale(BaseModel):
    date: date
    total_sales: int
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None
    is_forecast: bool = False  # True if forecast data, False if historical/actual data

# ========== ゲーミフィケーション関連スキーマ ==========

class GamificationProfileBase(BaseModel):
    contribution_points: int = 0
    total_earned_points: int = 0
    level: int = 1

class GamificationProfile(GamificationProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    criteria: Optional[Dict[str, Any]] = None
    is_active: bool = True

class BadgeCreate(BadgeBase):
    pass

class Badge(BadgeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBadge(BaseModel):
    id: int
    profile_id: int
    badge_id: int
    earned_at: datetime
    badge: Badge

    class Config:
        from_attributes = True

class PointTransactionBase(BaseModel):
    transaction_type: str  # "earn", "redeem", "exchange"
    points: int
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PointTransactionCreate(PointTransactionBase):
    pass

class PointTransaction(PointTransactionBase):
    id: int
    profile_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ========== レシート関連レスポンススキーマ ==========

class BadgeAwarded(BaseModel):
    badge_id: int
    badge_name: str
    is_new: bool

class PointDetails(BaseModel):
    base_points: int
    bonus_points: int
    bonus_details: List[Dict[str, Any]]

class ReceiptUploadResponse(BaseModel):
    receipt: Receipt
    points_earned: int
    point_details: PointDetails
    badges_awarded: List[BadgeAwarded]

# ========== LINE連携スキーマ ==========

class LineIntegrationBase(BaseModel):
    line_user_id: str
    line_display_name: Optional[str] = None
    is_active: bool = True

class LineIntegrationCreate(LineIntegrationBase):
    user_id: int

class LineIntegration(LineIntegrationBase):
    id: int
    user_id: int
    linked_at: datetime
    last_message_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========== 事業者関連スキーマ ==========

class StoreBase(BaseModel):
    name: str
    business_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StoreOwnerBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "owner"
    is_active: bool = True

class StoreOwnerCreate(StoreOwnerBase):
    password: str
    store_id: int

class StoreOwner(StoreOwnerBase):
    id: int
    store_id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    store: Store

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str
    start_date: datetime
    end_date: datetime
    discount_rate: Optional[float] = None
    coupon_code: Optional[str] = None
    target_products: Optional[List[str]] = None
    is_active: bool = True

class EventCreate(EventBase):
    store_id: int

class Event(EventBase):
    id: int
    store_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ArchiveContentBase(BaseModel):
    title: str
    content: Optional[str] = None
    content_type: str
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_published: bool = False

class ArchiveContentCreate(ArchiveContentBase):
    store_id: int

class ArchiveContent(ArchiveContentBase):
    id: int
    store_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ========== 特典・報酬システムスキーマ ==========

class RewardBase(BaseModel):
    title: str
    description: Optional[str] = None
    required_points: int
    reward_type: str  # 'coupon', 'gift', 'experience', 'digital'
    store_id: Optional[int] = None
    stock_quantity: Optional[int] = None
    is_active: bool = True
    is_featured: bool = False
    valid_days: int = 30
    terms_conditions: Optional[str] = None
    image_url: Optional[str] = None
    expires_at: Optional[datetime] = None

class RewardCreate(RewardBase):
    pass

class Reward(RewardBase):
    id: int
    available_stock: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserRewardBase(BaseModel):
    reward_id: int
    coupon_code: Optional[str] = None
    status: str = "active"
    expires_at: Optional[datetime] = None
    used_at: Optional[datetime] = None
    used_store_id: Optional[int] = None

class UserRewardCreate(BaseModel):
    reward_id: int

class UserReward(UserRewardBase):
    id: int
    user_id: int
    redeemed_points: int
    created_at: datetime
    reward: Reward

    class Config:
        from_attributes = True

# ========== ゲーミフィケーション拡張スキーマ ==========

class PointCalculationResult(BaseModel):
    base_points: int
    bonus_points: int
    total_points: int
    bonus_details: List[Dict[str, Any]] = []
    
class BadgeAwardResult(BaseModel):
    badge_id: int
    badge_name: str
    is_new: bool  # 新規獲得かどうか

# ========== 商品管理スキーマ ==========

class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    is_active: bool = True
    sort_order: int = 0

class ProductCategoryCreate(ProductCategoryBase):
    store_id: int

class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class ProductCategory(ProductCategoryBase):
    id: int
    store_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    product_code: Optional[str] = None
    unit_price: int
    cost_price: Optional[int] = None
    tax_rate: float = 0.10
    unit: str = "個"
    stock_quantity: int = 0
    low_stock_threshold: int = 10
    is_stock_managed: bool = True
    is_active: bool = True
    is_featured: bool = False
    is_seasonal: bool = False
    sale_start_date: Optional[datetime] = None
    sale_end_date: Optional[datetime] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    allergen_info: Optional[Dict[str, Any]] = None
    nutritional_info: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    store_id: int
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    product_code: Optional[str] = None
    unit_price: Optional[int] = None
    cost_price: Optional[int] = None
    tax_rate: Optional[float] = None
    unit: Optional[str] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    is_stock_managed: Optional[bool] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_seasonal: Optional[bool] = None
    sale_start_date: Optional[datetime] = None
    sale_end_date: Optional[datetime] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    allergen_info: Optional[Dict[str, Any]] = None
    nutritional_info: Optional[Dict[str, Any]] = None

class Product(ProductBase):
    id: int
    store_id: int
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[ProductCategory] = None

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    per_page: int
    total_pages: int

class ProductStockUpdate(BaseModel):
    product_id: int
    quantity_change: int  # 正の値=入庫、負の値=出庫
    reason: str  # "purchase", "sale", "adjustment", "return"
    notes: Optional[str] = None
