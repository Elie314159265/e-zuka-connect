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

@router.post("/fetch-and-store", status_code=201)
def fetch_and_store_weather_data(db: Session = Depends(get_db)):
    """
    過去1週間分の福岡地方の気象データを気象庁APIから取得し、DBに保存します。
    """
    try:
        # 気象庁の天気予報APIからデータを取得
        response = requests.get(JMA_FORECAST_URL)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch weather data: {str(e)}")

    # 天気データ（福岡地方）と気温データ（福岡市）を探す
    weather_data = None
    temp_data = None
    
    for forecast in data:
        time_series = forecast.get("timeSeries", [])
        for ts in time_series:
            areas = ts.get("areas", [])
            for area_data in areas:
                area_code = area_data.get("area", {}).get("code")
                # 天気データ（福岡地方）
                if area_code == FUKUOKA_AREA_CODE and "weathers" in area_data:
                    weather_data = {
                        "times": ts.get("timeDefines", []),
                        "weathers": area_data.get("weathers", []),
                        "weatherCodes": area_data.get("weatherCodes", [])
                    }
                # 気温データ（福岡市）
                elif area_code == FUKUOKA_CITY_CODE and "tempsMax" in area_data:
                    temp_data = {
                        "times": ts.get("timeDefines", []),
                        "tempsMax": area_data.get("tempsMax", []),
                        "tempsMin": area_data.get("tempsMin", [])
                    }

    if not weather_data or not weather_data["weathers"]:
        raise HTTPException(status_code=404, detail="Fukuoka weather data not found in JMA API response")

    stored_count = 0
    today = datetime.utcnow().date()
    
    # 天気データの時間軸をベースに処理
    for i, time_str in enumerate(weather_data["times"]):
        try:
            # ISO形式の日時をパース（タイムゾーンを考慮）
            weather_date = datetime.fromisoformat(time_str).date()
            
            # 今日以降のデータのみ処理（過去データは除外）
            if weather_date < today:
                continue
                
            # 既存データがないか確認
            if not crud.get_weather_data_by_date(db, weather_date.strftime('%Y-%m-%d')):
                # 気温データを検索（対応する日付のインデックスを探す）
                temp_max = temp_min = None
                if temp_data:
                    for j, temp_time_str in enumerate(temp_data["times"]):
                        temp_date = datetime.fromisoformat(temp_time_str).date()
                        if temp_date == weather_date:
                            try:
                                temp_max_str = temp_data["tempsMax"][j] if len(temp_data["tempsMax"]) > j else ""
                                temp_min_str = temp_data["tempsMin"][j] if len(temp_data["tempsMin"]) > j else ""
                                temp_max = float(temp_max_str) if temp_max_str and temp_max_str != "" else None
                                temp_min = float(temp_min_str) if temp_min_str and temp_min_str != "" else None
                            except (ValueError, IndexError):
                                temp_max = temp_min = None
                            break
                
                # 天気コードまたは天気文字列からWMOコードを生成
                weather_code = 3  # デフォルト: 曇り
                if len(weather_data["weatherCodes"]) > i:
                    # 気象庁の天気コードをWMOコードに変換（簡易版）
                    jma_code = weather_data["weatherCodes"][i]
                    weather_code = _map_jma_code_to_wmo_code(jma_code)
                elif len(weather_data["weathers"]) > i:
                    # 天気文字列からWMOコードを推定
                    weather_text = weather_data["weathers"][i]
                    weather_code = _map_jma_weather_to_wmo_code(weather_text)
                
                weather_data_create = schemas.WeatherDataCreate(
                    date=datetime.combine(weather_date, datetime.min.time()),
                    temperature_max=temp_max,
                    temperature_min=temp_min,
                    humidity=None,
                    weather_code=weather_code
                )
                crud.create_weather_data(db=db, weather=weather_data_create)
                stored_count += 1
                
        except (ValueError, IndexError) as e:
            # 個別の日付処理エラーは無視して続行
            continue
            
    return {"message": f"Successfully stored {stored_count} new weather data entries from JMA API."}
