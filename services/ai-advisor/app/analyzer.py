"""
統計分析エンジン
売上データ、気象データ、顧客情報を分析して洞察を抽出
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta


class SalesAnalyzer:
    """売上データ分析"""

    @staticmethod
    def analyze_sales_trend(daily_sales: List[Dict]) -> Dict[str, Any]:
        """
        売上トレンド分析
        Args:
            daily_sales: [{"date": "2025-09-30", "total_sales": 1200, "is_forecast": False}, ...]
        Returns:
            トレンド分析結果
        """
        if not daily_sales:
            return {"trend": "insufficient_data", "growth_rate": 0}

        # 実績データのみ抽出
        actual_sales = [s for s in daily_sales if not s.get("is_forecast", False) and s.get("total_sales", 0) > 0]

        if len(actual_sales) < 2:
            return {"trend": "insufficient_data", "growth_rate": 0}

        # 売上合計と平均
        total_sales = sum(s["total_sales"] for s in actual_sales)
        avg_sales = total_sales / len(actual_sales)

        # 前半と後半で比較（成長率計算）
        mid_point = len(actual_sales) // 2
        first_half = actual_sales[:mid_point]
        second_half = actual_sales[mid_point:]

        avg_first = sum(s["total_sales"] for s in first_half) / len(first_half) if first_half else 0
        avg_second = sum(s["total_sales"] for s in second_half) / len(second_half) if second_half else 0

        growth_rate = ((avg_second - avg_first) / avg_first * 100) if avg_first > 0 else 0

        # トレンド判定
        if growth_rate > 10:
            trend = "increasing"
        elif growth_rate < -10:
            trend = "decreasing"
        else:
            trend = "stable"

        # 最高売上日と最低売上日
        max_sales_day = max(actual_sales, key=lambda x: x["total_sales"])
        min_sales_day = min(actual_sales, key=lambda x: x["total_sales"])

        return {
            "trend": trend,
            "growth_rate": round(growth_rate, 2),
            "total_sales": total_sales,
            "avg_daily_sales": round(avg_sales, 2),
            "max_sales": max_sales_day["total_sales"],
            "max_sales_date": max_sales_day["date"],
            "min_sales": min_sales_day["total_sales"],
            "min_sales_date": min_sales_day["date"],
            "sales_volatility": round((max_sales_day["total_sales"] - min_sales_day["total_sales"]) / avg_sales * 100, 2)
        }

    @staticmethod
    def analyze_weather_impact(weather_data: Dict) -> Dict[str, Any]:
        """
        天候の売上への影響分析
        Args:
            weather_data: {"sunny_days_sales": 850, "rainy_days_sales": 720, ...}
        Returns:
            天候影響分析結果
        """
        sunny_sales = weather_data.get("sunny_days_sales", 0)
        rainy_sales = weather_data.get("rainy_days_sales", 0)

        if sunny_sales == 0 or rainy_sales == 0:
            return {"impact": "insufficient_data", "recommendation": "データ不足"}

        # 影響率計算
        impact_rate = ((sunny_sales - rainy_sales) / rainy_sales * 100)

        if abs(impact_rate) < 5:
            impact = "minimal"
            recommendation = "天候による売上の変動は小さいです。"
        elif impact_rate > 5:
            impact = "positive_sunny"
            recommendation = f"晴れの日は雨の日より約{abs(round(impact_rate))}%売上が高い傾向です。晴れの日に特別プロモーションを実施すると効果的です。"
        else:
            impact = "positive_rainy"
            recommendation = f"雨の日は晴れの日より約{abs(round(impact_rate))}%売上が高い傾向です。雨の日限定メニューや配達サービスの強化を検討してください。"

        return {
            "impact": impact,
            "impact_rate": round(impact_rate, 2),
            "recommendation": recommendation,
            "sunny_avg": round(sunny_sales, 2),
            "rainy_avg": round(rainy_sales, 2)
        }


class ProductAnalyzer:
    """商品分析"""

    @staticmethod
    def analyze_product_performance(rankings: Dict) -> Dict[str, Any]:
        """
        商品パフォーマンス分析
        Args:
            rankings: {"quantity_ranking": [...], "sales_ranking": [...]}
        Returns:
            商品分析結果
        """
        quantity_ranking = rankings.get("quantity_ranking", [])
        sales_ranking = rankings.get("sales_ranking", [])

        if not quantity_ranking or not sales_ranking:
            return {"status": "insufficient_data"}

        # トップ商品
        top_quantity = quantity_ranking[0] if quantity_ranking else None
        top_sales = sales_ranking[0] if sales_ranking else None

        # 高単価商品の特定（売上ランキング上位だが購入数は少ない）
        high_value_products = []
        for sales_item in sales_ranking[:5]:
            # 対応する購入数を探す
            qty_item = next((q for q in quantity_ranking if q["name"] == sales_item["name"]), None)
            if qty_item:
                avg_price = sales_item["value"] / qty_item["value"] if qty_item["value"] > 0 else 0
                if avg_price > 0:
                    high_value_products.append({
                        "name": sales_item["name"],
                        "avg_price": round(avg_price, 2),
                        "total_sales": sales_item["value"],
                        "quantity": qty_item["value"]
                    })

        # 平均単価が高い順にソート
        high_value_products.sort(key=lambda x: x["avg_price"], reverse=True)

        return {
            "status": "success",
            "top_seller_by_quantity": top_quantity,
            "top_seller_by_revenue": top_sales,
            "high_value_products": high_value_products[:3],
            "total_product_types": len(quantity_ranking)
        }

    @staticmethod
    def recommend_promotions(product_analysis: Dict, sales_trend: Dict) -> List[str]:
        """
        プロモーション推奨
        Args:
            product_analysis: 商品分析結果
            sales_trend: 売上トレンド分析結果
        Returns:
            推奨アクション
        """
        recommendations = []

        if product_analysis.get("status") != "success":
            return ["商品データが不足しています。"]

        # トップ商品のプッシュ
        top_qty = product_analysis.get("top_seller_by_quantity")
        if top_qty:
            recommendations.append(f"【人気商品】「{top_qty['name']}」は購入数1位です。目立つ位置に配置し、セット販売を検討してください。")

        # 高単価商品の推奨
        high_value = product_analysis.get("high_value_products", [])
        if high_value:
            top_high_value = high_value[0]
            recommendations.append(f"【高単価商品】「{top_high_value['name']}」は平均単価¥{int(top_high_value['avg_price'])}の高単価商品です。SNSでの紹介や試食キャンペーンで認知度を上げましょう。")

        # 売上トレンドに基づく推奨
        trend = sales_trend.get("trend")
        if trend == "decreasing":
            recommendations.append(f"【売上改善】直近の売上が{abs(sales_trend.get('growth_rate', 0)):.1f}%減少傾向です。新商品投入や期間限定キャンペーンで顧客の関心を引きましょう。")
        elif trend == "increasing":
            recommendations.append(f"【好調維持】売上が{sales_trend.get('growth_rate', 0):.1f}%増加中です。この勢いを維持するため、リピート促進のポイントカードやLINE友だち追加特典を強化しましょう。")

        # ボラティリティに基づく推奨
        volatility = sales_trend.get("sales_volatility", 0)
        if volatility > 50:
            recommendations.append(f"【売上安定化】日ごとの売上変動が大きい（{volatility:.1f}%）です。曜日別キャンペーンや定期購入プランで安定化を図りましょう。")

        return recommendations


class CustomerAnalyzer:
    """顧客分析"""

    @staticmethod
    def analyze_demographics(demographics: Dict) -> Dict[str, Any]:
        """
        顧客層分析
        Args:
            demographics: {"age_demographics": [...], "gender_demographics": [...]}
        Returns:
            顧客分析結果
        """
        age_demo = demographics.get("age_demographics", [])
        gender_demo = demographics.get("gender_demographics", [])

        if not age_demo or not gender_demo:
            return {"status": "insufficient_data"}

        # 主要顧客層
        top_age_group = max(age_demo, key=lambda x: x["value"]) if age_demo else None
        top_gender = max(gender_demo, key=lambda x: x["value"]) if gender_demo else None

        # 総顧客数
        total_customers = sum(d["value"] for d in age_demo)

        return {
            "status": "success",
            "primary_age_group": top_age_group,
            "primary_gender": top_gender,
            "total_customers": total_customers,
            "age_distribution": age_demo,
            "gender_distribution": gender_demo
        }

    @staticmethod
    def recommend_targeting(customer_analysis: Dict) -> List[str]:
        """
        ターゲティング推奨
        Args:
            customer_analysis: 顧客分析結果
        Returns:
            推奨ターゲティング戦略
        """
        recommendations = []

        if customer_analysis.get("status") != "success":
            return ["顧客データが不足しています。"]

        primary_age = customer_analysis.get("primary_age_group")
        primary_gender = customer_analysis.get("primary_gender")

        if primary_age:
            age_name = primary_age["name"]
            age_ratio = (primary_age["value"] / customer_analysis["total_customers"] * 100)
            recommendations.append(f"【主要顧客層】{age_name}が{age_ratio:.1f}%を占めています。この年代に人気の商品やSNSチャネル（Instagram, TikTokなど）を活用しましょう。")

        if primary_gender:
            gender_name = primary_gender["name"]
            gender_ratio = (primary_gender["value"] / customer_analysis["total_customers"] * 100)
            if gender_ratio > 60:
                recommendations.append(f"【性別偏り】{gender_name}が{gender_ratio:.1f}%と多数派です。他の性別層へのアプローチ（商品ラインナップの多様化、店舗雰囲気の見直し）も検討してください。")

        return recommendations


def generate_comprehensive_advice(
    daily_sales: List[Dict],
    weather_data: Dict,
    product_rankings: Dict,
    demographics: Dict
) -> Dict[str, Any]:
    """
    総合的な経営アドバイス生成
    Args:
        daily_sales: 日別売上データ
        weather_data: 天候別売上データ
        product_rankings: 商品ランキング
        demographics: 顧客層データ
    Returns:
        総合アドバイス
    """
    # 各分析を実行
    sales_trend = SalesAnalyzer.analyze_sales_trend(daily_sales)
    weather_impact = SalesAnalyzer.analyze_weather_impact(weather_data)
    product_analysis = ProductAnalyzer.analyze_product_performance(product_rankings)
    customer_analysis = CustomerAnalyzer.analyze_demographics(demographics)

    # 推奨アクション生成
    promotion_recommendations = ProductAnalyzer.recommend_promotions(product_analysis, sales_trend)
    targeting_recommendations = CustomerAnalyzer.recommend_targeting(customer_analysis)

    # 総合サマリー生成
    summary = f"""
【売上状況】
期間の総売上: ¥{sales_trend.get('total_sales', 0):,}
1日あたりの平均売上: ¥{int(sales_trend.get('avg_daily_sales', 0)):,}
売上トレンド: {_trend_to_japanese(sales_trend.get('trend', 'stable'))} ({sales_trend.get('growth_rate', 0):+.1f}%)

【天候の影響】
{weather_impact.get('recommendation', '分析データ不足')}

【商品分析】
最も売れている商品（購入数）: {product_analysis.get('top_seller_by_quantity', {}).get('name', 'データなし')}
最も売上貢献している商品: {product_analysis.get('top_seller_by_revenue', {}).get('name', 'データなし')}

【顧客層】
主要顧客層: {customer_analysis.get('primary_age_group', {}).get('name', 'データなし')}
総顧客数: {customer_analysis.get('total_customers', 0)}人
""".strip()

    return {
        "summary": summary,
        "recommendations": {
            "product_promotions": promotion_recommendations,
            "customer_targeting": targeting_recommendations,
            "weather_strategy": [weather_impact.get("recommendation", "")]
        },
        "analytics": {
            "sales_trend": sales_trend,
            "weather_impact": weather_impact,
            "product_performance": product_analysis,
            "customer_demographics": customer_analysis
        }
    }


def _trend_to_japanese(trend: str) -> str:
    """トレンドを日本語に変換"""
    mapping = {
        "increasing": "上昇傾向",
        "decreasing": "下降傾向",
        "stable": "安定",
        "insufficient_data": "データ不足"
    }
    return mapping.get(trend, "不明")