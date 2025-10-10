"""
LLM-based Advisory System using Google Gemini API
Gemini APIを使用したAI経営アドバイス生成
"""
import os
import logging
from typing import Dict, Any, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiAdvisor:
    """Gemini APIを使った経営アドバイス生成クラス"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        Args:
            api_key: Google API Key (環境変数 GOOGLE_API_KEY から取得可能)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("Gemini API initialized successfully")
        else:
            self.model = None
            logger.warning("GOOGLE_API_KEY not found. LLM features will be disabled.")

    def is_available(self) -> bool:
        """LLM機能が利用可能かチェック"""
        return self.model is not None

    def generate_advice(
        self,
        sales_trend: Dict[str, Any],
        weather_impact: Dict[str, Any],
        product_analysis: Dict[str, Any],
        customer_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI経営アドバイス生成
        Args:
            sales_trend: 売上トレンド分析結果
            weather_impact: 天候影響分析結果
            product_analysis: 商品分析結果
            customer_analysis: 顧客分析結果
        Returns:
            生成されたアドバイス
        """
        if not self.is_available():
            raise ValueError("Gemini API is not configured. Set GOOGLE_API_KEY environment variable.")

        # プロンプト生成
        prompt = self._build_prompt(sales_trend, weather_impact, product_analysis, customer_analysis)

        try:
            # Gemini API呼び出し（安全設定を調整）
            from google.generativeai.types import HarmCategory, HarmBlockThreshold

            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                ),
                safety_settings=safety_settings
            )

            # レスポンス確認
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError(f"No valid response: finish_reason={response.candidates[0].finish_reason if response.candidates else 'NO_CANDIDATES'}")

            advice_text = response.text

            # 構造化されたレスポンスを生成
            return self._parse_advice_response(
                advice_text,
                sales_trend,
                weather_impact,
                product_analysis,
                customer_analysis
            )

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    def _build_prompt(
        self,
        sales_trend: Dict[str, Any],
        weather_impact: Dict[str, Any],
        product_analysis: Dict[str, Any],
        customer_analysis: Dict[str, Any]
    ) -> str:
        """分析データからプロンプトを構築"""

        # データ整形
        total_sales = sales_trend.get('total_sales', 0)
        avg_sales = sales_trend.get('avg_daily_sales', 0)
        growth_rate = sales_trend.get('growth_rate', 0)
        trend = sales_trend.get('trend', 'stable')

        weather_rec = weather_impact.get('recommendation', 'データ不足')
        impact_rate = weather_impact.get('impact_rate', 0)

        top_product_qty = product_analysis.get('top_seller_by_quantity', {})
        top_product_rev = product_analysis.get('top_seller_by_revenue', {})
        high_value_products = product_analysis.get('high_value_products', [])

        primary_age = customer_analysis.get('primary_age_group', {})
        primary_gender = customer_analysis.get('primary_gender', {})
        total_customers = customer_analysis.get('total_customers', 0)

        prompt = f"""店舗の売上データを分析し、今後の運営に役立つ提案をお願いします。

期間の売上データ:
総売上は{int(total_sales)}円で、1日平均{int(avg_sales)}円です。売上は{self._trend_to_japanese(trend)}で、成長率は{growth_rate:.1f}パーセントです。

天候との関係:
晴れの日の平均売上は{int(weather_impact.get('sunny_avg', 0))}円、雨の日は{int(weather_impact.get('rainy_avg', 0))}円でした。

商品について:
よく売れている商品は{top_product_qty.get('name', '不明')}で、売上金額が最も大きい商品は{top_product_rev.get('name', '不明')}です。

お客様について:
来店されたお客様は合計{total_customers}名で、主な年齢層は{primary_age.get('name', '不明')}です。

以下の項目について、具体的で実行可能な内容を日本語で教えてください:

1. 現在の状況についての所感
2. 今後取り組むべき施策を3つ
3. 商品とお客様に関する提案
4. 短期的な目標と中期的な目標
"""

        return prompt

    def _parse_advice_response(
        self,
        advice_text: str,
        sales_trend: Dict[str, Any],
        weather_impact: Dict[str, Any],
        product_analysis: Dict[str, Any],
        customer_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        LLMの応答をパースして構造化
        """
        # LLMの出力をそのままsummaryとして使用
        summary = advice_text

        # LLM出力を行ごとに分割して推奨事項を抽出
        lines = advice_text.split('\n')
        product_promotions = []
        customer_targeting = []
        weather_strategy = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('【'):
                continue
            # 番号付きリストまたは「-」で始まる行を抽出
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('・')):
                # キーワードで分類
                if '商品' in line or '売れ' in line or 'メニュー' in line or 'セット' in line:
                    product_promotions.append(line)
                elif '客' in line or '年代' in line or '性別' in line or 'SNS' in line or 'ターゲット' in line:
                    customer_targeting.append(line)
                elif '天' in line or '雨' in line or '晴' in line or '気象' in line:
                    weather_strategy.append(line)
                else:
                    # デフォルトは商品戦略に
                    product_promotions.append(line)

        # 空の場合は全文を商品戦略に入れる
        if not product_promotions and not customer_targeting and not weather_strategy:
            product_promotions = [advice_text]

        recommendations = {
            "ai_generated_advice": [advice_text],
            "product_promotions": product_promotions,
            "customer_targeting": customer_targeting,
            "weather_strategy": weather_strategy if weather_strategy else [weather_impact.get('recommendation', '')]
        }

        # 元の分析データも含める
        analytics = {
            "sales_trend": sales_trend,
            "weather_impact": weather_impact,
            "product_performance": product_analysis,
            "customer_demographics": customer_analysis,
            "ai_generated": True
        }

        return {
            "summary": summary,
            "recommendations": recommendations,
            "analytics": analytics
        }

    @staticmethod
    def _trend_to_japanese(trend: str) -> str:
        """トレンドを日本語に変換"""
        mapping = {
            "increasing": "上昇傾向",
            "decreasing": "下降傾向",
            "stable": "安定",
            "insufficient_data": "データ不足"
        }
        return mapping.get(trend, "不明")


# グローバルインスタンス（シングルトンパターン）
_gemini_advisor_instance = None


def get_gemini_advisor() -> GeminiAdvisor:
    """GeminiAdvisorのシングルトンインスタンスを取得"""
    global _gemini_advisor_instance
    if _gemini_advisor_instance is None:
        _gemini_advisor_instance = GeminiAdvisor()
    return _gemini_advisor_instance
