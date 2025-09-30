"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowLeft, TrendingUp, Calendar, DollarSign, Package, Users, AlertTriangle } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useAuthStore } from '../../store/authStore';

const pageVariants = {
    initial: { opacity: 0, y: 20 },
    in: { opacity: 1, y: 0 },
    out: { opacity: 0, y: -20 }
};

const pageTransition = {
    type: "tween",
    ease: "anticipate",
    duration: 0.5
} as const;

interface DailySale {
    date: string;
    total_sales: number;
    temperature_max?: number;
    temperature_min?: number;
    is_forecast?: boolean;
}

interface ProductRanking {
    name: string;
    value: number;
}

interface ProductRankings {
    quantity_ranking: ProductRanking[];
    sales_ranking: ProductRanking[];
}

interface Demographics {
    name: string;
    value: number;
}

interface SalesByWeather {
    sunny_days_sales: number;
    rainy_days_sales: number;
    sunny_days_count: number;
    rainy_days_count: number;
}

export default function SalesAnalyticsPage() {
    const [dailySales, setDailySales] = useState<DailySale[]>([]);
    const [productRankings, setProductRankings] = useState<ProductRankings>({ quantity_ranking: [], sales_ranking: [] });
    const [demographics, setDemographics] = useState<{ age: Demographics[], gender: Demographics[] }>({ age: [], gender: [] });
    const [weatherAnalysis, setWeatherAnalysis] = useState<SalesByWeather | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { token } = useAuthStore();

    useEffect(() => {
        const fetchData = async () => {
            if (!token) {
                setError("認証トークンがありません。再度ログインしてください。");
                setIsLoading(false);
                return;
            }

            try {
                const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://your-gcp-project-id.com';

                const [dailySalesRes, rankingsRes, demographicsRes, weatherRes] = await Promise.all([
                    fetch(`${apiBaseUrl}/api/analysis/daily-sales?days_back=30&days_forward=7`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/product-rankings?limit=10`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/customer-demographics`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/sales-by-weather`, { headers: { 'Authorization': `Bearer ${token}` } })
                ]);

                if (!dailySalesRes.ok || !rankingsRes.ok || !demographicsRes.ok || !weatherRes.ok) {
                    const errorRes = [dailySalesRes, rankingsRes, demographicsRes, weatherRes].find(res => !res.ok);
                    const errorData = errorRes ? await errorRes.json() : { detail: 'データの取得に失敗しました。' };
                    throw new Error(errorData.detail);
                }

                const dailySalesData: DailySale[] = await dailySalesRes.json();
                const rankingsData: ProductRankings = await rankingsRes.json();
                const demographicsData = await demographicsRes.json();
                const weatherData: SalesByWeather = await weatherRes.json();

                setDailySales(dailySalesData.map(d => ({
                    ...d,
                    date: new Date(d.date).toLocaleDateString('ja-JP', { month: 'numeric', day: 'numeric' })
                })));
                setProductRankings(rankingsData);
                setDemographics({
                    age: demographicsData.age_demographics,
                    gender: demographicsData.gender_demographics
                });
                setWeatherAnalysis(weatherData);

            } catch (err) {
                setError(err instanceof Error ? err.message : '不明なエラーが発生しました。');
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [token]);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF6B9D', '#4ECDC4', '#95E1D3'];

    // 過去のデータのみを抽出（売上がある実績データ）
    const pastSalesData = dailySales.filter(d => d.total_sales > 0 && !d.is_forecast);

    // 売上統計計算
    const totalSales = pastSalesData.reduce((sum, d) => sum + d.total_sales, 0);
    const averageSales = pastSalesData.length > 0 ? totalSales / pastSalesData.length : 0;
    const maxSales = pastSalesData.length > 0 ? Math.max(...pastSalesData.map(d => d.total_sales)) : 0;

    if (isLoading) {
        return (
            <motion.div
                className="min-h-screen bg-gray-100 py-24 flex items-center justify-center"
                initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
            >
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">売上分析データを読み込み中...</p>
                </div>
            </motion.div>
        );
    }

    if (error) {
        return (
            <motion.div
                className="min-h-screen bg-gray-100 py-24 flex items-center justify-center"
                initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
            >
                <div className="text-center">
                    <AlertTriangle className="w-16 h-16 text-red-600 mx-auto mb-4" />
                    <p className="text-red-600 text-xl mb-4">{error}</p>
                    <Link href="/dashboard" className="text-blue-600 hover:text-blue-800">ダッシュボードに戻る</Link>
                </div>
            </motion.div>
        );
    }

    return (
        <motion.div
            className="min-h-screen bg-gray-100 py-24"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="container mx-auto px-6">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div className="flex items-center">
                        <Link href="/dashboard" className="mr-4">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="flex items-center text-gray-600 hover:text-gray-900"
                            >
                                <ArrowLeft className="w-6 h-6 mr-2" />
                                ダッシュボードに戻る
                            </motion.button>
                        </Link>
                        <h1 className="text-4xl font-bold text-gray-900">売上分析</h1>
                    </div>
                    <div className="text-sm text-gray-500">
                        <Calendar className="w-4 h-4 inline mr-1" />
                        過去30日間のデータ
                    </div>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <motion.div
                        whileHover={{ scale: 1.02 }}
                        className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-gray-500 text-sm mb-1">総売上</p>
                                <p className="text-3xl font-bold text-gray-900">¥{totalSales.toLocaleString()}</p>
                            </div>
                            <DollarSign className="w-12 h-12 text-blue-500" />
                        </div>
                    </motion.div>

                    <motion.div
                        whileHover={{ scale: 1.02 }}
                        className="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-500"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-gray-500 text-sm mb-1">平均日次売上</p>
                                <p className="text-3xl font-bold text-gray-900">¥{Math.round(averageSales).toLocaleString()}</p>
                            </div>
                            <TrendingUp className="w-12 h-12 text-green-500" />
                        </div>
                    </motion.div>

                    <motion.div
                        whileHover={{ scale: 1.02 }}
                        className="bg-white p-6 rounded-xl shadow-md border-l-4 border-purple-500"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-gray-500 text-sm mb-1">最高売上日</p>
                                <p className="text-3xl font-bold text-gray-900">¥{maxSales.toLocaleString()}</p>
                            </div>
                            <TrendingUp className="w-12 h-12 text-purple-500" />
                        </div>
                    </motion.div>

                    <motion.div
                        whileHover={{ scale: 1.02 }}
                        className="bg-white p-6 rounded-xl shadow-md border-l-4 border-orange-500"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-gray-500 text-sm mb-1">販売日数</p>
                                <p className="text-3xl font-bold text-gray-900">{pastSalesData.length}日</p>
                            </div>
                            <Calendar className="w-12 h-12 text-orange-500" />
                        </div>
                    </motion.div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column - Sales Chart */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Daily Sales Chart */}
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h3 className="font-bold text-xl mb-4 flex items-center">
                                <TrendingUp className="w-6 h-6 mr-2 text-blue-600" />
                                日別売上推移（過去30日間）
                            </h3>
                            <ResponsiveContainer width="100%" height={400}>
                                <LineChart data={dailySales} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="date" />
                                    <YAxis yAxisId="sales" orientation="left" />
                                    <YAxis yAxisId="temp" orientation="right" />
                                    <Tooltip
                                        formatter={(value, name) => {
                                            const nameStr = String(name);
                                            if (nameStr.includes('売上')) return [`¥${value?.toLocaleString()}`, name];
                                            if (nameStr.includes('気温')) return [`${value}°C`, name];
                                            return [value, name];
                                        }}
                                    />
                                    <Legend />
                                    <Line
                                        yAxisId="sales"
                                        type="monotone"
                                        dataKey={(d) => d.total_sales > 0 ? d.total_sales : null}
                                        name="売上"
                                        stroke="#3B82F6"
                                        strokeWidth={3}
                                        dot={{ fill: '#3B82F6', r: 4 }}
                                        connectNulls={false}
                                    />
                                    <Line
                                        yAxisId="temp"
                                        type="monotone"
                                        dataKey={(d) => !d.is_forecast ? d.temperature_max : null}
                                        name="最高気温（実測）"
                                        stroke="#F59E0B"
                                        strokeWidth={2}
                                        connectNulls={false}
                                    />
                                    <Line
                                        yAxisId="temp"
                                        type="monotone"
                                        dataKey={(d) => d.is_forecast ? d.temperature_max : null}
                                        name="最高気温（予測）"
                                        stroke="#F59E0B"
                                        strokeWidth={2}
                                        strokeDasharray="5 5"
                                        strokeOpacity={0.6}
                                        connectNulls={true}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Product Rankings Bar Chart */}
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h3 className="font-bold text-xl mb-4 flex items-center">
                                <Package className="w-6 h-6 mr-2 text-purple-600" />
                                商品別売上ランキング TOP10
                            </h3>
                            <ResponsiveContainer width="100%" height={400}>
                                <BarChart data={productRankings.sales_ranking} margin={{ top: 5, right: 20, left: 20, bottom: 80 }}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                                    <YAxis />
                                    <Tooltip formatter={(value) => [`¥${value?.toLocaleString()}`, '売上']} />
                                    <Bar dataKey="value" fill="#8B5CF6" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Weather Impact */}
                        {weatherAnalysis && (
                            <div className="bg-white p-6 rounded-xl shadow-md">
                                <h3 className="font-bold text-xl mb-4">天候の売上への影響</h3>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                                        <p className="text-sm text-gray-600 mb-2">晴れの日の平均売上</p>
                                        <p className="text-3xl font-bold text-yellow-700">¥{Math.round(weatherAnalysis.sunny_days_sales).toLocaleString()}</p>
                                        <p className="text-sm text-gray-500 mt-2">{weatherAnalysis.sunny_days_count}日間</p>
                                    </div>
                                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                                        <p className="text-sm text-gray-600 mb-2">雨の日の平均売上</p>
                                        <p className="text-3xl font-bold text-blue-700">¥{Math.round(weatherAnalysis.rainy_days_sales).toLocaleString()}</p>
                                        <p className="text-sm text-gray-500 mt-2">{weatherAnalysis.rainy_days_count}日間</p>
                                    </div>
                                </div>
                                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                                    <p className="text-sm text-gray-700">
                                        {weatherAnalysis.sunny_days_sales > weatherAnalysis.rainy_days_sales
                                            ? `晴れの日は雨の日より平均${Math.round(((weatherAnalysis.sunny_days_sales - weatherAnalysis.rainy_days_sales) / weatherAnalysis.rainy_days_sales) * 100)}%売上が高い傾向があります。`
                                            : `雨の日は晴れの日より平均${Math.round(((weatherAnalysis.rainy_days_sales - weatherAnalysis.sunny_days_sales) / weatherAnalysis.sunny_days_sales) * 100)}%売上が高い傾向があります。`
                                        }
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Right Column - Rankings and Demographics */}
                    <div className="space-y-8">
                        {/* Purchase Quantity Ranking */}
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h3 className="font-bold text-xl mb-4 flex items-center">
                                <Package className="w-6 h-6 mr-2 text-green-600" />
                                人気商品ランキング TOP10
                            </h3>
                            {productRankings.quantity_ranking.length > 0 ? (
                                <ul className="space-y-3">
                                    {productRankings.quantity_ranking.map((item, index) => (
                                        <li key={index} className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition">
                                            <div className="flex items-center flex-1">
                                                <span className={`text-lg font-bold mr-4 w-8 ${
                                                    index === 0 ? 'text-yellow-500' :
                                                    index === 1 ? 'text-gray-400' :
                                                    index === 2 ? 'text-orange-400' : 'text-gray-500'
                                                }`}>
                                                    {index + 1}
                                                </span>
                                                <span className="text-gray-700">{item.name}</span>
                                            </div>
                                            <span className="text-sm font-semibold text-green-600">{item.value}個</span>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="text-gray-500 text-center py-4">データがありません</p>
                            )}
                        </div>

                        {/* Customer Demographics */}
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h3 className="font-bold text-xl mb-4 flex items-center">
                                <Users className="w-6 h-6 mr-2 text-indigo-600" />
                                顧客層分析
                            </h3>

                            {/* Age Demographics */}
                            {demographics.age.length > 0 && (
                                <div className="mb-6">
                                    <h4 className="font-semibold mb-3 text-gray-700">年代別</h4>
                                    <ResponsiveContainer width="100%" height={200}>
                                        <PieChart>
                                            <Pie
                                                data={demographics.age}
                                                dataKey="value"
                                                nameKey="name"
                                                cx="50%"
                                                cy="50%"
                                                outerRadius={70}
                                                fill="#8884d8"
                                                label={(entry) => `${entry.name}: ${entry.value}`}
                                            >
                                                {demographics.age.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            )}

                            {/* Gender Demographics */}
                            {demographics.gender.length > 0 && (
                                <div>
                                    <h4 className="font-semibold mb-3 text-gray-700">性別</h4>
                                    <ResponsiveContainer width="100%" height={200}>
                                        <PieChart>
                                            <Pie
                                                data={demographics.gender}
                                                dataKey="value"
                                                nameKey="name"
                                                cx="50%"
                                                cy="50%"
                                                outerRadius={70}
                                                fill="#82ca9d"
                                                label={(entry) => `${entry.name}: ${entry.value}`}
                                            >
                                                {demographics.gender.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            )}

                            {demographics.age.length === 0 && demographics.gender.length === 0 && (
                                <p className="text-gray-500 text-center py-4">データがありません</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}