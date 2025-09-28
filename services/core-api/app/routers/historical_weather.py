from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/historical-weather",
    tags=["historical-weather"],
)

# Open-Meteo API設定
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FUKUOKA_LAT = 33.5904
FUKUOKA_LON = 130.4017

def _calculate_weather_code_from_precipitation(precipitation: float, temperature: float) -> int:
    """
    降水量と気温から簡易的な天気コードを推定
    """
    if precipitation == 0:
        return 0  # Clear sky
    elif precipitation < 2.5:
        return 61  # Slight rain
    elif precipitation < 10:
        return 63  # Moderate rain
    else:
        return 65  # Heavy rain

@router.get("/", response_model=List[schemas.HistoricalWeatherData])
def read_historical_weather_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    過去気象データ一覧を取得します。
    """
    return crud.get_historical_weather_data(db, skip=skip, limit=limit)

@router.get("/range", response_model=List[schemas.HistoricalWeatherData])
def read_historical_weather_data_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    """
    指定日付範囲の過去気象データを取得します。
    Args:
        start_date: 開始日 (YYYY-MM-DD)
        end_date: 終了日 (YYYY-MM-DD)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    return crud.get_historical_weather_data_in_date_range(db, start, end)

@router.post("/fetch-and-store", status_code=201)
def fetch_and_store_historical_weather_data(
    weeks_back: int = 7,
    db: Session = Depends(get_db)
):
    """
    Open-Meteo APIから過去の気象データを取得してデータベースに保存します。
    Args:
        weeks_back: 何週間前まで取得するか（デフォルト7週間）
    """
    try:
        # 日付範囲を計算
        today = datetime.now().date()
        start_date = today - timedelta(weeks=weeks_back)
        end_date = today - timedelta(days=1)  # 昨日まで

        # Open-Meteo Archive APIに日次データをリクエスト
        params = {
            "latitude": FUKUOKA_LAT,
            "longitude": FUKUOKA_LON,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "precipitation_sum",
                "rain_sum",
                "snowfall_sum",
                "wind_speed_10m_max",
                "wind_direction_10m_dominant"
            ],
            "timezone": "Asia/Tokyo"
        }

        response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch historical weather data: {str(e)}")

    if "daily" not in data:
        raise HTTPException(status_code=404, detail="No daily weather data found in API response")

    daily_data = data["daily"]
    stored_count = 0
    updated_count = 0
    errors = []

    # 各日のデータを処理
    for i, date_str in enumerate(daily_data.get("time", [])):
        try:
            # 日付をパース
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

            # 各値を安全に取得
            temp_max = daily_data.get("temperature_2m_max", [None] * len(daily_data["time"]))[i]
            temp_min = daily_data.get("temperature_2m_min", [None] * len(daily_data["time"]))[i]
            temp_mean = daily_data.get("temperature_2m_mean", [None] * len(daily_data["time"]))[i]
            precipitation = daily_data.get("precipitation_sum", [None] * len(daily_data["time"]))[i]
            rain = daily_data.get("rain_sum", [None] * len(daily_data["time"]))[i]
            snowfall = daily_data.get("snowfall_sum", [None] * len(daily_data["time"]))[i]
            wind_speed = daily_data.get("wind_speed_10m_max", [None] * len(daily_data["time"]))[i]
            wind_direction = daily_data.get("wind_direction_10m_dominant", [None] * len(daily_data["time"]))[i]

            # 簡易的な天気コード計算
            weather_code = None
            if precipitation is not None and temp_mean is not None:
                weather_code = _calculate_weather_code_from_precipitation(precipitation, temp_mean)

            # データベース用オブジェクト作成
            historical_data = schemas.HistoricalWeatherDataCreate(
                date=date_obj,
                temperature_max=temp_max,
                temperature_min=temp_min,
                temperature_mean=temp_mean,
                precipitation_sum=precipitation,
                rain_sum=rain,
                snowfall_sum=snowfall,
                wind_speed_max=wind_speed,
                wind_direction=int(wind_direction) if wind_direction is not None else None,
                weather_code=weather_code,
                data_source="open-meteo"
            )

            # UPSERT実行
            existing = crud.get_historical_weather_data_by_date(db, date_obj.strftime('%Y-%m-%d'))
            if existing:
                # 既存データを更新
                for key, value in historical_data.dict(exclude={'date'}).items():
                    if value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                db.commit()
                updated_count += 1
            else:
                # 新規作成
                crud.create_historical_weather_data(db, historical_data)
                stored_count += 1

        except Exception as e:
            errors.append(f"Error processing {date_str}: {str(e)}")
            continue

    return {
        "message": f"Historical weather data collection completed.",
        "date_range": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        "weeks_processed": weeks_back,
        "stored_count": stored_count,
        "updated_count": updated_count,
        "total_days": len(daily_data.get("time", [])),
        "errors": errors[:5],  # 最大5個のエラーを表示
        "data_source": "open-meteo"
    }

@router.post("/manual-data", status_code=201)
def create_manual_historical_weather_data(
    weather_data: schemas.HistoricalWeatherDataCreate,
    db: Session = Depends(get_db)
):
    """
    過去気象データを手動で登録します。
    """
    existing_data = crud.get_historical_weather_data_by_date(
        db, weather_data.date.strftime('%Y-%m-%d')
    )

    if existing_data:
        raise HTTPException(
            status_code=400,
            detail=f"Historical weather data for {weather_data.date.strftime('%Y-%m-%d')} already exists"
        )

    db_weather = crud.create_historical_weather_data(db=db, weather=weather_data)
    return {
        "message": f"Successfully created historical weather data for {weather_data.date.strftime('%Y-%m-%d')}",
        "data": db_weather
    }

@router.delete("/cleanup", status_code=200)
def cleanup_historical_weather_data(
    older_than_weeks: int = 12,
    db: Session = Depends(get_db)
):
    """
    指定した週数より古い過去気象データを削除します。
    Args:
        older_than_weeks: この週数より古いデータを削除（デフォルト12週間）
    """
    cutoff_date = datetime.now().date() - timedelta(weeks=older_than_weeks)
    deleted_count = crud.delete_historical_weather_data_in_range(
        db,
        datetime(2020, 1, 1).date(),  # 十分古い日付
        cutoff_date
    )

    return {
        "message": f"Successfully deleted {deleted_count} historical weather data entries older than {older_than_weeks} weeks.",
        "cutoff_date": cutoff_date.strftime('%Y-%m-%d')
    }