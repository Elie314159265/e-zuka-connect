from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from typing import List
from datetime import date, timedelta

from .. import crud, schemas, security, models
from ..security.auth import get_current_store_owner
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
def get_sales_by_weather(db: Session = Depends(get_db), current_owner: models.StoreOwner = Depends(get_current_store_owner)):
    """
    天気ごとの売上分析データを取得します。
    晴れ（WMOコード 0-3）と雨（WMOコード 51以上）で分類します。
    """

    # 晴れの日の売上合計
    sunny_sales_query = db.query(func.sum(models.Receipt.total_amount)).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code <= 3,
        models.Receipt.store_id == current_owner.store_id
    )
    total_sunny_sales = sunny_sales_query.scalar() or 0

    # 晴れの日の日数
    sunny_days_query = db.query(func.count(func.distinct(func.date(models.Receipt.receipt_date)))).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code <= 3,
        models.Receipt.store_id == current_owner.store_id
    )
    count_sunny_days = sunny_days_query.scalar() or 0

    # 雨の日の売上合計
    rainy_sales_query = db.query(func.sum(models.Receipt.total_amount)).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code >= 51,
        models.Receipt.store_id == current_owner.store_id
    )
    total_rainy_sales = rainy_sales_query.scalar() or 0

    # 雨の日の日数
    rainy_days_query = db.query(func.count(func.distinct(func.date(models.Receipt.receipt_date)))).join(models.WeatherData, func.date(models.Receipt.receipt_date) == func.date(models.WeatherData.date)).filter(
        models.WeatherData.weather_code >= 51,
        models.Receipt.store_id == current_owner.store_id
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
    current_owner: models.StoreOwner = Depends(get_current_store_owner),
    days_back: int = 7,
    days_forward: int = 7
):
    """
    過去days_back日分と未来days_forward日分の日別売上データと気象データを取得します。
    実測データ: 昨日から過去days_back日分（historical_weather_data）
    予測データ: 今日から未来days_forward日分（weather_data）
    """

    today = date.today()
    yesterday = today - timedelta(days=1)

    # 実測データの範囲: 昨日から過去7日間（気温データ）
    historical_start = yesterday - timedelta(days=days_back - 1)
    historical_end = yesterday

    # 売上データの範囲: 今日を含む（今日の売上も表示）
    sales_start = historical_start
    sales_end = today

    # 予測データの範囲: 明日から未来7日間
    forecast_start = today + timedelta(days=1)
    forecast_end = today + timedelta(days=days_forward)

    # 過去のデータ（実測値 + 売上）- historical_weather_dataを使用
    # 売上は今日まで含める
    historical_sales = db.query(
        func.cast(models.Receipt.receipt_date, Date).label("date"),
        func.sum(models.Receipt.total_amount).label("total_sales"),
        models.HistoricalWeatherData.temperature_max,
        models.HistoricalWeatherData.temperature_min
    ).outerjoin(
        models.HistoricalWeatherData,
        func.cast(models.Receipt.receipt_date, Date) == func.cast(models.HistoricalWeatherData.date, Date)
    ).filter(
        func.cast(models.Receipt.receipt_date, Date) >= sales_start,
        func.cast(models.Receipt.receipt_date, Date) <= sales_end,
        models.Receipt.store_id == current_owner.store_id
    ).group_by(
        func.cast(models.Receipt.receipt_date, Date),
        models.HistoricalWeatherData.temperature_max,
        models.HistoricalWeatherData.temperature_min
    ).order_by(
        func.cast(models.Receipt.receipt_date, Date)
    ).all()

    # 売上がない日も含めるため、historical_weather_dataから全日付を取得
    all_historical_dates = db.query(
        func.cast(models.HistoricalWeatherData.date, Date).label("date"),
        models.HistoricalWeatherData.temperature_max,
        models.HistoricalWeatherData.temperature_min
    ).filter(
        func.cast(models.HistoricalWeatherData.date, Date) >= historical_start,
        func.cast(models.HistoricalWeatherData.date, Date) <= historical_end
    ).order_by(
        func.cast(models.HistoricalWeatherData.date, Date)
    ).all()

    # 売上データを辞書化
    sales_by_date = {row.date: row.total_sales for row in historical_sales}

    # 未来のデータ（予測値のみ）- weather_dataを使用
    forecast_weather = db.query(
        func.cast(models.WeatherData.date, Date).label("date"),
        models.WeatherData.temperature_max,
        models.WeatherData.temperature_min
    ).filter(
        func.cast(models.WeatherData.date, Date) >= forecast_start,
        func.cast(models.WeatherData.date, Date) <= forecast_end
    ).order_by(
        func.cast(models.WeatherData.date, Date)
    ).all()

    # 結果をDailySaleモデルに変換
    result = []

    # 過去データ（実測）- 全日付を含める
    for row in all_historical_dates:
        result.append(schemas.DailySale(
            date=row.date,
            total_sales=sales_by_date.get(row.date, 0),
            temperature_max=row.temperature_max,
            temperature_min=row.temperature_min,
            is_forecast=False
        ))

    # 今日のデータ（売上あり、気温は予測データから取得）
    today_sales = sales_by_date.get(today, 0)
    if today_sales > 0 or True:  # 今日は常に追加
        # 今日の気温予測データを取得
        today_weather = db.query(
            models.WeatherData.temperature_max,
            models.WeatherData.temperature_min
        ).filter(
            func.cast(models.WeatherData.date, Date) == today
        ).first()

        result.append(schemas.DailySale(
            date=today,
            total_sales=today_sales,
            temperature_max=today_weather.temperature_max if today_weather else None,
            temperature_min=today_weather.temperature_min if today_weather else None,
            is_forecast=True  # 気温は予測値（売上は実測だが、気温データに合わせて予測扱い）
        ))

    # 未来データ（予測）- 明日以降
    for row in forecast_weather:
        result.append(schemas.DailySale(
            date=row.date,
            total_sales=0,  # 未来の売上は0
            temperature_max=row.temperature_max,
            temperature_min=row.temperature_min,
            is_forecast=True
        ))

    return result

@router.get("/customer-demographics")
def get_customer_demographics(db: Session = Depends(get_db), current_owner: models.StoreOwner = Depends(get_current_store_owner)):
    """
    レシートを投稿したユーザーの客層（年代、性別）を分析します。
    """

    # このオーナーの店で買い物をしたユニークな顧客のIDリストを取得
    customer_ids = db.query(
        models.Receipt.user_id
    ).filter(
        models.Receipt.store_id == current_owner.store_id
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

@router.get("/product-rankings")
def get_product_rankings(db: Session = Depends(get_db), current_owner: models.StoreOwner = Depends(get_current_store_owner), limit: int = 5):
    """
    商品の購入数ランキングと売上ランキングを取得します。
    """

    # 購入数ランキング（descriptionごとの個数集計）
    quantity_ranking = db.query(
        models.ReceiptItem.description,
        func.count(models.ReceiptItem.id).label("quantity")
    ).join(
        models.Receipt, models.ReceiptItem.receipt_id == models.Receipt.id
    ).filter(
        models.Receipt.store_id == current_owner.store_id,
        models.ReceiptItem.description.isnot(None),
        models.ReceiptItem.description != ""
    ).group_by(
        models.ReceiptItem.description
    ).order_by(
        func.count(models.ReceiptItem.id).desc()
    ).limit(limit).all()

    # 売上ランキング（descriptionごとの金額合計）
    sales_ranking = db.query(
        models.ReceiptItem.description,
        func.sum(models.ReceiptItem.amount).label("total_sales")
    ).join(
        models.Receipt, models.ReceiptItem.receipt_id == models.Receipt.id
    ).filter(
        models.Receipt.store_id == current_owner.store_id,
        models.ReceiptItem.description.isnot(None),
        models.ReceiptItem.description != "",
        models.ReceiptItem.amount.isnot(None)
    ).group_by(
        models.ReceiptItem.description
    ).order_by(
        func.sum(models.ReceiptItem.amount).desc()
    ).limit(limit).all()

    return {
        "quantity_ranking": [{"name": desc, "value": int(qty)} for desc, qty in quantity_ranking],
        "sales_ranking": [{"name": desc, "value": int(sales)} for desc, sales in sales_ranking],
    }
