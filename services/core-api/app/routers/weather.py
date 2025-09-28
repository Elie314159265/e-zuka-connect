from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

# 気象庁API設定
JMA_FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json"
FUKUOKA_PREFECTURE_CODE = "400000"
FUKUOKA_AREA_CODE = "400010"  # 福岡地方（天気情報）
FUKUOKA_CITY_CODE = "82182"   # 福岡市（気温情報）

def _map_jma_weather_to_wmo_code(weather_text: str) -> int:
    """
    気象庁の天気文字列をWMO天気コードにマッピングします。
    """
    weather_text = weather_text.lower()
    
    # 晴れ系
    if "晴" in weather_text or "快晴" in weather_text:
        return 0  # Clear sky
    elif "薄曇" in weather_text or "うす曇" in weather_text:
        return 1  # Mainly clear
    elif "曇" in weather_text:
        if "時々晴" in weather_text or "一時晴" in weather_text:
            return 2  # Partly cloudy
        else:
            return 3  # Overcast
    
    # 雨系
    elif "雨" in weather_text:
        if "大雨" in weather_text or "激しい雨" in weather_text:
            return 65  # Heavy rain
        elif "強い雨" in weather_text:
            return 63  # Moderate rain
        else:
            return 61  # Slight rain
    
    # 雪系
    elif "雪" in weather_text:
        if "大雪" in weather_text:
            return 75  # Heavy snow
        elif "みぞれ" in weather_text:
            return 68  # Slight rain and snow mixed
        else:
            return 71  # Slight snow fall
    
    # 雷・嵐系
    elif "雷" in weather_text or "嵐" in weather_text:
        return 95  # Thunderstorm
    
    # 霧系
    elif "霧" in weather_text:
        return 45  # Fog
    
    # デフォルトは曇り
    else:
        return 3  # Overcast

def _map_jma_code_to_wmo_code(jma_code: str) -> int:
    """
    気象庁の天気コードをWMO天気コードにマッピングします。
    """
    try:
        code = int(jma_code)
    except (ValueError, TypeError):
        return 3  # デフォルト: 曇り
    
    # 気象庁天気コードからWMOコードへの簡易マッピング
    if code == 100 or code == 101:  # 晴れ、晴れ時々曇り
        return 0  # Clear sky
    elif code == 110 or code == 111:  # 晴れ後曇り、晴れ後雨
        return 1  # Mainly clear
    elif code == 200 or code == 201:  # 曇り、曇り時々晴れ
        return 2  # Partly cloudy
    elif code == 210 or code == 211:  # 曇り後晴れ、曇り後雨
        return 3  # Overcast
    elif 300 <= code <= 350:  # 雨系
        if code == 300 or code == 301:  # 雨、雨時々晴れ
            return 61  # Slight rain
        elif code == 311 or code == 313:  # 雨後曇り、雨後晴れ
            return 63  # Moderate rain
        else:
            return 65  # Heavy rain
    elif 400 <= code <= 450:  # 雪系
        return 71  # Slight snow fall
    elif code >= 200 and "雷" in str(code):  # 雷を含む
        return 95  # Thunderstorm
    else:
        return 3  # デフォルト: 曇り

@router.get("/", response_model=List[schemas.WeatherData])
def read_weather_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    データベースに保存されている気象データを取得します。
    """
    weather_data = crud.get_weather_data(db, skip=skip, limit=limit)
    return weather_data

@router.get("/recent", response_model=List[schemas.WeatherData])
def read_recent_weather_data(days: int = 7, db: Session = Depends(get_db)):
    """
    過去の手動データと未来の予報データを統合して、指定日数分の気象データを取得します。
    Args:
        days: 取得する日数（デフォルト7日、今日を含む前後の日数）
    """
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=days-1)  # 例：7日なら6日前から今日まで
    end_date = today + timedelta(days=days-1)    # 例：7日なら今日から6日後まで

    weather_data = crud.get_weather_data_in_date_range(db, start_date, end_date)
    return weather_data

@router.post("/fetch-and-store", status_code=201)
def fetch_and_store_weather_data(db: Session = Depends(get_db)):
    """
    福岡地方の気象データ（今日以降の予報）を気象庁APIから取得し、
    UPSERT処理で既存データを更新または新規作成します。
    拡張: より多くの未来日付データを取得し、詳細なログを提供します。
    """
    try:
        # 気象庁の天気予報APIからデータを取得
        response = requests.get(JMA_FORECAST_URL)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch weather data: {str(e)}")

    # すべての天気データと気温データを収集
    all_weather_data = []
    all_temp_data = []

    for forecast in data:
        time_series = forecast.get("timeSeries", [])
        for ts in time_series:
            areas = ts.get("areas", [])
            for area_data in areas:
                area_code = area_data.get("area", {}).get("code")
                # 天気データ（福岡地方）
                if area_code == FUKUOKA_AREA_CODE and "weathers" in area_data:
                    all_weather_data.append({
                        "times": ts.get("timeDefines", []),
                        "weathers": area_data.get("weathers", []),
                        "weatherCodes": area_data.get("weatherCodes", [])
                    })
                # 気温データ（福岡市）
                elif area_code == FUKUOKA_CITY_CODE and "tempsMax" in area_data:
                    all_temp_data.append({
                        "times": ts.get("timeDefines", []),
                        "tempsMax": area_data.get("tempsMax", []),
                        "tempsMin": area_data.get("tempsMin", [])
                    })

    if not all_weather_data:
        raise HTTPException(status_code=404, detail="Fukuoka weather data not found in JMA API response")

    stored_count = 0

    # 日付ベースのデータマップを作成
    weather_by_date = {}
    temp_by_date = {}

    # すべての天気データを日付でインデックス化（日付フィルタリングなし）
    for weather_data in all_weather_data:
        for i, time_str in enumerate(weather_data["times"]):
            try:
                # JSTの時刻文字列から日付を抽出（タイムゾーン情報は自動的に処理される）
                weather_date = datetime.fromisoformat(time_str).date()
                if weather_date not in weather_by_date:
                    weather_by_date[weather_date] = {}

                    # 天気コード
                    if len(weather_data["weatherCodes"]) > i:
                        weather_by_date[weather_date]["weather_code"] = weather_data["weatherCodes"][i]

                    # 天気文字列
                    if len(weather_data["weathers"]) > i:
                        weather_by_date[weather_date]["weather_text"] = weather_data["weathers"][i]
            except (ValueError, IndexError):
                continue

    # すべての気温データを日付でインデックス化（日付フィルタリングなし）
    for temp_data in all_temp_data:
        for i, time_str in enumerate(temp_data["times"]):
            try:
                # JSTの時刻文字列から日付を抽出（タイムゾーン情報は自動的に処理される）
                temp_date = datetime.fromisoformat(time_str).date()
                if temp_date not in temp_by_date:
                    temp_by_date[temp_date] = {}

                    # 最高気温
                    if len(temp_data["tempsMax"]) > i:
                        temp_max_str = temp_data["tempsMax"][i]
                        if temp_max_str and temp_max_str != "":
                            try:
                                temp_by_date[temp_date]["temp_max"] = float(temp_max_str)
                            except ValueError:
                                pass

                    # 最低気温
                    if len(temp_data["tempsMin"]) > i:
                        temp_min_str = temp_data["tempsMin"][i]
                        if temp_min_str and temp_min_str != "":
                            try:
                                temp_by_date[temp_date]["temp_min"] = float(temp_min_str)
                            except ValueError:
                                pass
            except (ValueError, IndexError):
                continue

    # 統合データを作成
    all_dates = set(weather_by_date.keys()) | set(temp_by_date.keys())
    processed_dates = []

    for weather_date in sorted(all_dates):
        # 天気コード取得
        weather_code = 3  # デフォルト: 曇り
        weather_info = weather_by_date.get(weather_date, {})

        if "weather_code" in weather_info:
            weather_code = _map_jma_code_to_wmo_code(weather_info["weather_code"])
        elif "weather_text" in weather_info:
            weather_code = _map_jma_weather_to_wmo_code(weather_info["weather_text"])

        # 気温データ取得
        temp_info = temp_by_date.get(weather_date, {})
        temp_max = temp_info.get("temp_max")
        temp_min = temp_info.get("temp_min")

        try:
            weather_data_create = schemas.WeatherDataCreate(
                date=datetime.combine(weather_date, datetime.min.time()),
                temperature_max=temp_max,
                temperature_min=temp_min,
                humidity=None,
                weather_code=weather_code
            )
            crud.upsert_weather_data(db=db, weather=weather_data_create)
            stored_count += 1
            processed_dates.append(weather_date.strftime('%Y-%m-%d'))
        except Exception as e:
            continue

    # 実際の処理範囲を計算
    if processed_dates:
        actual_start_date = min(processed_dates)
        actual_end_date = max(processed_dates)
        actual_date_range = f"{actual_start_date} to {actual_end_date}"
    else:
        actual_date_range = "No data processed"

    # デバッグ情報を含むレスポンス
    return {
        "message": f"Successfully upserted {stored_count} weather data entries from JMA API.",
        "processed_dates": processed_dates,
        "actual_date_range": actual_date_range,
        "note": "Processing all available dates from JMA API timeDefines",
        "weather_sources": len(all_weather_data),
        "temp_sources": len(all_temp_data)
    }

@router.post("/manual-data", status_code=201)
def create_manual_weather_data(weather_data: schemas.WeatherDataCreate, db: Session = Depends(get_db)):
    """
    過去の気象データを手動で登録します。
    """
    # 同じ日付のデータが既に存在するかチェック
    existing_data = crud.get_weather_data_by_date(db, weather_data.date.strftime('%Y-%m-%d'))
    if existing_data:
        raise HTTPException(status_code=400, detail=f"Weather data for {weather_data.date.strftime('%Y-%m-%d')} already exists")

    db_weather = crud.create_weather_data(db=db, weather=weather_data)
    return {"message": f"Successfully created weather data for {weather_data.date.strftime('%Y-%m-%d')}", "data": db_weather}

@router.post("/bulk-manual-data", status_code=201)
def create_bulk_manual_weather_data(weather_data_list: List[schemas.WeatherDataCreate], db: Session = Depends(get_db)):
    """
    過去の気象データを一括で手動登録します。
    """
    created_count = 0
    skipped_count = 0
    errors = []

    for weather_data in weather_data_list:
        try:
            # 同じ日付のデータが既に存在するかチェック
            existing_data = crud.get_weather_data_by_date(db, weather_data.date.strftime('%Y-%m-%d'))
            if existing_data:
                skipped_count += 1
                continue

            crud.create_weather_data(db=db, weather=weather_data)
            created_count += 1

        except Exception as e:
            errors.append(f"Error for {weather_data.date.strftime('%Y-%m-%d')}: {str(e)}")

    return {
        "message": f"Bulk insert completed. Created: {created_count}, Skipped: {skipped_count}",
        "created_count": created_count,
        "skipped_count": skipped_count,
        "errors": errors
    }

@router.delete("/cleanup", status_code=200)
def cleanup_old_weather_data(days_to_keep: int = 7, db: Session = Depends(get_db)):
    """
    指定した日数より古い天気データを削除します。
    Args:
        days_to_keep: 保持する日数（デフォルト7日）
    """
    deleted_count = crud.delete_old_weather_data(db, days_to_keep=days_to_keep)
    return {"message": f"Successfully deleted {deleted_count} weather data entries older than {days_to_keep} days."}
