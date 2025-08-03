from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from typing import List
from datetime import date, timedelta

from .. import crud, schemas, security, models
from ..database import get_db

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)

class SalesByWeatherResponse(schemas.BaseModel):
    sunny_days_sales: float
    rainy_days_sales: float
    sunny_days_count: int
    rainy_days_count: int


@router.get("/sales-by-weather", response_model=SalesByWeatherResponse)
def get_sales_by_weather(db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    """
    天気ごとの売上分析データを取得します。
    晴れ（WMOコード 0-3）と雨（WMOコード 51以上）で分類します。
    """
    if not current_user.is_owner:
        raise HTTPException(status_code=403, detail="Not authorized for this operation.")

    # 晴れの日の売上合計
    sunny_sales_query = db.query(func.sum(models.Receipt.total_amount)).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code <= 3
    )
    total_sunny_sales = sunny_sales_query.scalar() or 0

    # 晴れの日の日数
    sunny_days_query = db.query(func.count(func.distinct(func.date(models.Receipt.receipt_date)))).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code <= 3
    )
    count_sunny_days = sunny_days_query.scalar() or 0
    
    # 雨の日の売上合計
    rainy_sales_query = db.query(func.sum(models.Receipt.total_amount)).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code >= 51
    )
    total_rainy_sales = rainy_sales_query.scalar() or 0

    # 雨の日の日数
    rainy_days_query = db.query(func.count(func.distinct(func.date(models.Receipt.receipt_date)))).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code >= 51
    )
    count_rainy_days = rainy_days_query.scalar() or 0

    avg_sunny_sales = total_sunny_sales / count_sunny_days if count_sunny_days > 0 else 0
    avg_rainy_sales = total_rainy_sales / count_rainy_days if count_rainy_days > 0 else 0

    return {
        "sunny_days_sales": avg_sunny_sales,
        "rainy_days_sales": avg_rainy_sales,
        "sunny_days_count": count_sunny_days,
        "rainy_days_count": count_rainy_days,
    }

@router.get("/daily-sales", response_model=List[schemas.DailySale])
def get_daily_sales(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user),
    days: int = 30
):
    """
    指定された日数分の日別売上データを取得します。
    """
    if not current_user.is_owner:
        raise HTTPException(status_code=403, detail="Not authorized for this operation.")

    start_date = date.today() - timedelta(days=days)

    # 売上データと気温データをJOINして取得
    sales_data = db.query(
        func.cast(models.Receipt.receipt_date, Date).label("date"),
        func.sum(models.Receipt.total_amount).label("total_sales"),
        models.WeatherData.temperature_max,
        models.WeatherData.temperature_min
    ).outerjoin(
        models.WeatherData, 
        func.cast(models.Receipt.receipt_date, Date) == func.cast(models.WeatherData.date, Date)
    ).filter(
        func.cast(models.Receipt.receipt_date, Date) >= start_date
    ).group_by(
        func.cast(models.Receipt.receipt_date, Date),
        models.WeatherData.temperature_max,
        models.WeatherData.temperature_min
    ).order_by(
        func.cast(models.Receipt.receipt_date, Date)
    ).all()

    # 結果をDailySaleモデルに変換
    result = []
    for row in sales_data:
        result.append(schemas.DailySale(
            date=row.date,
            total_sales=row.total_sales or 0,
            temperature_max=row.temperature_max,
            temperature_min=row.temperature_min
        ))
    
    return result

@router.get("/customer-demographics")
def get_customer_demographics(db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    """
    レシートを投稿したユーザーの客層（年代、性別）を分析します。
    """
    if not current_user.is_owner:
        raise HTTPException(status_code=403, detail="Not authorized for this operation.")

    # このオーナーの店で買い物をしたユニークな顧客のIDリストを取得
    customer_ids = db.query(
        models.Receipt.user_id
    ).filter(
        models.Receipt.supplier_name == current_user.full_name # 仮。店舗IDで紐づけるのが望ましい
    ).distinct().all()
    
    customer_id_list = [c[0] for c in customer_ids]

    if not customer_id_list:
        return {"age_demographics": [], "gender_demographics": []}

    # 年代別集計
    age_demographics = db.query(
        models.User.age_group,
        func.count(models.User.id).label("count")
    ).filter(
        models.User.id.in_(customer_id_list)
    ).group_by(models.User.age_group).all()

    # 性別集計
    gender_demographics = db.query(
        models.User.gender,
        func.count(models.User.id).label("count")
    ).filter(
        models.User.id.in_(customer_id_list)
    ).group_by(models.User.gender).all()

    return {
        "age_demographics": [{"name": age or "未設定", "value": count} for age, count in age_demographics],
        "gender_demographics": [{"name": gender or "未設定", "value": count} for gender, count in gender_demographics],
    }
