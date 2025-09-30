"use client";
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, TrendingUp, CloudRain, ShoppingBag, Users } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

interface AiAdviceModalProps {
    isOpen: boolean;
    onClose: () => void;
}

interface AdviceResponse {
    summary: string;
    recommendations: {
        product_promotions: string[];
        customer_targeting: string[];
        weather_strategy: string[];
    };
    analytics: {
        sales_trend: {
            trend: string;
            growth_rate: number;
            avg_daily_sales: number;
            total_sales: number;
            max_sales: number;
            max_sales_date: string;
            min_sales: number;
            min_sales_date: string;
        };
        weather_impact: {
            impact: string;
            impact_rate?: number;
            recommendation?: string;
            sunny_avg?: number;
            rainy_avg?: number;
        };
        product_performance: {
            status: string;
            top_seller_by_quantity?: { name: string; value: number };
            top_seller_by_revenue?: { name: string; value: number };
            high_value_products: Array<{ name: string; avg_price: number }>;
        };
        customer_demographics: {
            status: string;
            primary_age_group?: { name: string; value: number };
            primary_gender?: { name: string; value: number };
            total_customers: number;
        };
    };
}

export default function AiAdviceModal({ isOpen, onClose }: AiAdviceModalProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [adviceData, setAdviceData] = useState<AdviceResponse | null>(null);
    const [error, setError] = useState('');
    const { token } = useAuthStore();

    const fetchAdvice = async () => {
        setIsLoading(true);
        setAdviceData(null);
        setError('');

        try {
            const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://your-gcp-project-id.com';

            const response = await fetch(`${apiBaseUrl}/api/ai-advice/generate`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'AIアドバイスの取得に失敗しました。');
            }

            const result: AdviceResponse = await response.json();
            setAdviceData(result);
        } catch (err) {
            console.error("Error calling AI Advisor API:", err);
            setError(err instanceof Error ? err.message : 'AIからのアドバイスの取得に失敗しました。');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchAdvice();
        }
    }, [isOpen]);

    const getTrendLabel = (trend: string) => {
        const mapping: { [key: string]: string } = {
            'increasing': '増加傾向',
            'decreasing': '減少傾向',
            'stable': '安定',
            'insufficient_data': 'データ不足'
        };
        return mapping[trend] || trend;
    };

    const getImpactLabel = (impact: string) => {
        const mapping: { [key: string]: string } = {
            'positive_sunny': '晴れの日が有利',
            'positive_rainy': '雨の日が有利',
            'minimal': '影響小',
            'insufficient_data': 'データ不足'
        };
        return mapping[impact] || impact;
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="fixed inset-0 bg-black/60 z-[110] flex items-center justify-center p-4 backdrop-blur-sm"
                >
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        onClick={(e) => e.stopPropagation()}
                        className="bg-white rounded-2xl shadow-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto p-8 relative"
                    >
                        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 z-10">
                            <X className="w-6 h-6" />
                        </button>
                        <div className="text-center mb-6">
                            <Sparkles className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                            <h2 className="text-2xl font-bold mb-2">AI経営アドバイザー</h2>
                            <p className="text-gray-600 text-sm">あなたの店舗データを総合的に分析しました</p>
                        </div>
                        <div className="text-left">
                            {isLoading && (
                                <div className="flex flex-col items-center justify-center h-48">
                                    <motion.div
                                        animate={{ rotate: 360 }}
                                        transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                                        className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full"
                                    />
                                    <p className="mt-4 text-gray-500">AIが分析中です...</p>
                                </div>
                            )}
                            {error && (
                                <div className="text-red-500 text-center bg-red-50 p-4 rounded-lg">
                                    <p className="font-semibold">エラーが発生しました</p>
                                    <p className="text-sm mt-2">{error}</p>
                                </div>
                            )}
                            {adviceData && (
                                <div className="space-y-6">
                                    {/* サマリー */}
                                    <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-100">
                                        <h3 className="font-bold text-lg mb-2 text-purple-900">📊 総合分析サマリー</h3>
                                        <p className="text-gray-700 leading-relaxed">{adviceData.summary}</p>
                                    </div>

                                    {/* 売上トレンド */}
                                    <div className="bg-blue-50 p-5 rounded-xl border border-blue-100">
                                        <div className="flex items-center mb-3">
                                            <TrendingUp className="w-6 h-6 text-blue-600 mr-2" />
                                            <h3 className="font-bold text-lg text-blue-900">売上トレンド</h3>
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-600">傾向:</span>
                                                <span className={`font-semibold ${
                                                    adviceData.analytics.sales_trend.trend === 'increasing' ? 'text-green-600' :
                                                    adviceData.analytics.sales_trend.trend === 'decreasing' ? 'text-red-600' :
                                                    'text-gray-600'
                                                }`}>{getTrendLabel(adviceData.analytics.sales_trend.trend)}</span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-600">成長率:</span>
                                                <span className={`font-semibold ${
                                                    adviceData.analytics.sales_trend.growth_rate > 0 ? 'text-green-600' :
                                                    adviceData.analytics.sales_trend.growth_rate < 0 ? 'text-red-600' :
                                                    'text-gray-600'
                                                }`}>{adviceData.analytics.sales_trend.growth_rate.toFixed(1)}%</span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-600">平均日売上:</span>
                                                <span className="font-semibold text-blue-700">¥{adviceData.analytics.sales_trend.avg_daily_sales.toLocaleString()}</span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-600">合計売上:</span>
                                                <span className="font-semibold text-blue-700">¥{adviceData.analytics.sales_trend.total_sales.toLocaleString()}</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* 天気の影響 */}
                                    <div className="bg-sky-50 p-5 rounded-xl border border-sky-100">
                                        <div className="flex items-center mb-3">
                                            <CloudRain className="w-6 h-6 text-sky-600 mr-2" />
                                            <h3 className="font-bold text-lg text-sky-900">天気の影響</h3>
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-600">影響度:</span>
                                                <span className="font-semibold text-sky-600">{getImpactLabel(adviceData.analytics.weather_impact.impact)}</span>
                                            </div>
                                            {adviceData.analytics.weather_impact.impact_rate !== undefined && (
                                                <div className="flex items-center justify-between">
                                                    <span className="text-gray-600">影響率:</span>
                                                    <span className="font-semibold text-sky-600">{adviceData.analytics.weather_impact.impact_rate.toFixed(1)}%</span>
                                                </div>
                                            )}
                                            {adviceData.analytics.weather_impact.sunny_avg !== undefined && (
                                                <div className="flex items-center justify-between">
                                                    <span className="text-gray-600">晴れの日平均:</span>
                                                    <span className="font-semibold text-yellow-600">¥{adviceData.analytics.weather_impact.sunny_avg.toLocaleString()}</span>
                                                </div>
                                            )}
                                            {adviceData.analytics.weather_impact.rainy_avg !== undefined && (
                                                <div className="flex items-center justify-between">
                                                    <span className="text-gray-600">雨の日平均:</span>
                                                    <span className="font-semibold text-blue-600">¥{adviceData.analytics.weather_impact.rainy_avg.toLocaleString()}</span>
                                                </div>
                                            )}
                                            {adviceData.analytics.weather_impact.recommendation && (
                                                <div className="mt-3 text-sm text-gray-700 pl-4 border-l-2 border-sky-300">
                                                    {adviceData.analytics.weather_impact.recommendation}
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* 商品インサイト */}
                                    {adviceData.analytics.product_performance.status === 'success' && (
                                        <div className="bg-amber-50 p-5 rounded-xl border border-amber-100">
                                            <div className="flex items-center mb-3">
                                                <ShoppingBag className="w-6 h-6 text-amber-600 mr-2" />
                                                <h3 className="font-bold text-lg text-amber-900">商品インサイト</h3>
                                            </div>
                                            <div className="space-y-2">
                                                {adviceData.analytics.product_performance.top_seller_by_quantity && (
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-gray-600">人気No.1:</span>
                                                        <span className="font-semibold text-amber-700">
                                                            {adviceData.analytics.product_performance.top_seller_by_quantity.name}
                                                        </span>
                                                    </div>
                                                )}
                                                {adviceData.analytics.product_performance.top_seller_by_revenue && (
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-gray-600">売上No.1:</span>
                                                        <span className="font-semibold text-amber-700">
                                                            {adviceData.analytics.product_performance.top_seller_by_revenue.name}
                                                        </span>
                                                    </div>
                                                )}
                                                {adviceData.analytics.product_performance.high_value_products.length > 0 && (
                                                    <div className="mt-3">
                                                        <span className="text-gray-600 block mb-2">高単価商品:</span>
                                                        <ul className="space-y-1 pl-4">
                                                            {adviceData.analytics.product_performance.high_value_products.map((product, idx) => (
                                                                <li key={idx} className="text-sm text-gray-700">
                                                                    {product.name} (平均¥{product.avg_price.toLocaleString()})
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* 顧客インサイト */}
                                    {adviceData.analytics.customer_demographics.status === 'success' && (
                                        <div className="bg-green-50 p-5 rounded-xl border border-green-100">
                                            <div className="flex items-center mb-3">
                                                <Users className="w-6 h-6 text-green-600 mr-2" />
                                                <h3 className="font-bold text-lg text-green-900">顧客インサイト</h3>
                                            </div>
                                            <div className="space-y-2">
                                                {adviceData.analytics.customer_demographics.primary_age_group && (
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-gray-600">主な年代:</span>
                                                        <span className="font-semibold text-green-700">
                                                            {adviceData.analytics.customer_demographics.primary_age_group.name}
                                                        </span>
                                                    </div>
                                                )}
                                                {adviceData.analytics.customer_demographics.primary_gender && (
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-gray-600">主な性別:</span>
                                                        <span className="font-semibold text-green-700">
                                                            {adviceData.analytics.customer_demographics.primary_gender.name}
                                                        </span>
                                                    </div>
                                                )}
                                                <div className="flex items-center justify-between">
                                                    <span className="text-gray-600">総顧客数:</span>
                                                    <span className="font-semibold text-green-700">
                                                        {adviceData.analytics.customer_demographics.total_customers}人
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    {/* アクションプラン */}
                                    <div className="bg-gradient-to-r from-rose-50 to-pink-50 p-5 rounded-xl border border-rose-100">
                                        <h3 className="font-bold text-lg mb-3 text-rose-900">💡 推奨アクションプラン</h3>
                                        <div className="space-y-4">
                                            {/* 商品プロモーション */}
                                            {adviceData.recommendations.product_promotions.length > 0 && (
                                                <div>
                                                    <h4 className="font-semibold text-rose-800 mb-2">商品戦略:</h4>
                                                    <ul className="space-y-2">
                                                        {adviceData.recommendations.product_promotions.map((rec, index) => (
                                                            <li key={index} className="flex items-start">
                                                                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-rose-200 text-rose-800 font-semibold text-sm mr-3 flex-shrink-0 mt-0.5">
                                                                    {index + 1}
                                                                </span>
                                                                <span className="text-gray-700 leading-relaxed">{rec}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                            {/* 顧客ターゲティング */}
                                            {adviceData.recommendations.customer_targeting.length > 0 && (
                                                <div>
                                                    <h4 className="font-semibold text-rose-800 mb-2">顧客戦略:</h4>
                                                    <ul className="space-y-2">
                                                        {adviceData.recommendations.customer_targeting.map((rec, index) => (
                                                            <li key={index} className="flex items-start">
                                                                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-pink-200 text-pink-800 font-semibold text-sm mr-3 flex-shrink-0 mt-0.5">
                                                                    {index + 1}
                                                                </span>
                                                                <span className="text-gray-700 leading-relaxed">{rec}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                            {/* 天候戦略 */}
                                            {adviceData.recommendations.weather_strategy.length > 0 && adviceData.recommendations.weather_strategy[0] && (
                                                <div>
                                                    <h4 className="font-semibold text-rose-800 mb-2">天候対応:</h4>
                                                    <div className="text-gray-700 leading-relaxed pl-4 border-l-2 border-rose-300">
                                                        {adviceData.recommendations.weather_strategy[0]}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}