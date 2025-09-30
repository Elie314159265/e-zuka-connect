"""
AI Advisor Service - FastAPI Application
経営アドバイス生成サービス
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from .analyzer import generate_comprehensive_advice

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Advisor Service",
    description="e-ZUKA CONNECT 経営アドバイス生成サービス",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエストモデル
class DailySale(BaseModel):
    date: str
    total_sales: float
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None
    is_forecast: Optional[bool] = False


class WeatherData(BaseModel):
    sunny_days_sales: float
    rainy_days_sales: float
    sunny_days_count: int
    rainy_days_count: int


class ProductRanking(BaseModel):
    name: str
    value: int


class ProductRankings(BaseModel):
    quantity_ranking: List[ProductRanking]
    sales_ranking: List[ProductRanking]


class Demographics(BaseModel):
    name: str
    value: int


class DemographicsData(BaseModel):
    age_demographics: List[Demographics]
    gender_demographics: List[Demographics]


class AdviceRequest(BaseModel):
    daily_sales: List[DailySale]
    weather_data: WeatherData
    product_rankings: ProductRankings
    demographics: DemographicsData


# レスポンスモデル
class AdviceResponse(BaseModel):
    summary: str
    recommendations: Dict[str, List[str]]
    analytics: Dict[str, Any]


@app.get("/")
def root():
    """ヘルスチェック"""
    return {
        "service": "AI Advisor Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}


@app.post("/api/advice/generate", response_model=AdviceResponse)
async def generate_advice(request: AdviceRequest):
    """
    経営アドバイス生成エンドポイント

    売上データ、天候データ、商品ランキング、顧客層データを分析し、
    総合的な経営アドバイスを生成します。
    """
    try:
        logger.info("経営アドバイス生成リクエストを受信")

        # データを辞書形式に変換
        daily_sales_dict = [sale.model_dump() for sale in request.daily_sales]
        weather_data_dict = request.weather_data.model_dump()
        product_rankings_dict = request.product_rankings.model_dump()
        demographics_dict = request.demographics.model_dump()

        # 総合アドバイス生成
        advice = generate_comprehensive_advice(
            daily_sales=daily_sales_dict,
            weather_data=weather_data_dict,
            product_rankings=product_rankings_dict,
            demographics=demographics_dict
        )

        logger.info("経営アドバイス生成完了")
        return advice

    except Exception as e:
        logger.error(f"アドバイス生成中にエラーが発生: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"アドバイス生成に失敗しました: {str(e)}"
        )


@app.post("/api/advice/quick-insights")
async def quick_insights(request: AdviceRequest):
    """
    簡易インサイト生成（軽量版）

    主要な指標のみを素早く返します。
    """
    try:
        from .analyzer import SalesAnalyzer, ProductAnalyzer, CustomerAnalyzer

        daily_sales_dict = [sale.model_dump() for sale in request.daily_sales]
        product_rankings_dict = request.product_rankings.model_dump()

        # 売上トレンドと商品分析のみ実行
        sales_trend = SalesAnalyzer.analyze_sales_trend(daily_sales_dict)
        product_analysis = ProductAnalyzer.analyze_product_performance(product_rankings_dict)

        return {
            "avg_daily_sales": sales_trend.get("avg_daily_sales", 0),
            "growth_rate": sales_trend.get("growth_rate", 0),
            "trend": sales_trend.get("trend", "stable"),
            "top_product": product_analysis.get("top_seller_by_quantity", {}).get("name", "データなし")
        }

    except Exception as e:
        logger.error(f"簡易インサイト生成中にエラー: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"インサイト生成に失敗しました: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)