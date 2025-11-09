from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import httpx
import logging

from .. import models
from ..security.auth import get_current_store_owner
from ..database import get_db
from . import analysis

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/ai-advice",
    tags=["ai-advice"],
)

# AI Advisor Serviceのエンドポイント
AI_ADVISOR_SERVICE_URL = "http://ai-advisor-service.e-zuka-connect.svc.cluster.local:8002"


@router.post("/generate")
async def generate_ai_advice(
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
) -> Dict[str, Any]:
    """
    AI経営アドバイスを生成

    店舗の売上データ、天候データ、商品ランキング、顧客層データを分析し、
    総合的な経営アドバイスを生成します。
    """
    try:
        logger.info(f"AI経営アドバイス生成開始: store_id={current_owner.store_id}")

        # 既存のanalysisエンドポイントからデータを取得
        # 日別売上データ
        from .analysis import get_daily_sales, get_sales_by_weather, get_customer_demographics, get_product_rankings

        daily_sales_data = get_daily_sales(db=db, current_owner=current_owner, days_back=30, days_forward=7)
        weather_data = get_sales_by_weather(db=db, current_owner=current_owner)
        demographics_data = get_customer_demographics(db=db, current_owner=current_owner)
        rankings_data = get_product_rankings(db=db, current_owner=current_owner, limit=10)

        # AI Advisor Serviceにリクエストを送信
        request_payload = {
            "daily_sales": [
                {
                    "date": str(sale.date),
                    "total_sales": float(sale.total_sales),
                    "temperature_max": float(sale.temperature_max) if sale.temperature_max else None,
                    "temperature_min": float(sale.temperature_min) if sale.temperature_min else None,
                    "is_forecast": bool(sale.is_forecast)
                }
                for sale in daily_sales_data
            ],
            "weather_data": {
                "sunny_days_sales": float(weather_data["sunny_days_sales"]),
                "rainy_days_sales": float(weather_data["rainy_days_sales"]),
                "sunny_days_count": int(weather_data["sunny_days_count"]),
                "rainy_days_count": int(weather_data["rainy_days_count"])
            },
            "product_rankings": {
                "quantity_ranking": [
                    {"name": item["name"], "value": item["value"]}
                    for item in rankings_data["quantity_ranking"]
                ],
                "sales_ranking": [
                    {"name": item["name"], "value": item["value"]}
                    for item in rankings_data["sales_ranking"]
                ]
            },
            "demographics": {
                "age_demographics": demographics_data["age_demographics"],
                "gender_demographics": demographics_data["gender_demographics"]
            }
        }

        # AI Advisor Serviceを呼び出し
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_ADVISOR_SERVICE_URL}/api/advice/generate",
                json=request_payload
            )

            if response.status_code != 200:
                logger.error(f"AI Advisor Service error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=502,
                    detail="AI経営アドバイスの生成に失敗しました"
                )

            advice_result = response.json()
            logger.info("AI経営アドバイス生成完了")

            return advice_result

    except httpx.TimeoutException:
        logger.error("AI Advisor Service timeout")
        raise HTTPException(
            status_code=504,
            detail="AI経営アドバイスの生成がタイムアウトしました"
        )
    except httpx.RequestError as e:
        logger.error(f"AI Advisor Service request error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail="AI経営アドバイスサービスに接続できませんでした"
        )
    except Exception as e:
        logger.error(f"AI経営アドバイス生成中にエラー: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI経営アドバイスの生成中にエラーが発生しました: {str(e)}"
        )