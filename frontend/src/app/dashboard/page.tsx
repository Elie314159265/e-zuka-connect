"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Sparkles, Sun, CloudRain, BarChart3, PieChart as PieChartIcon, AlertTriangle, Package, Settings, Users } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, Sector } from 'recharts';
import AiAdviceModal from '../../components/AiAdviceModal';
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

interface SalesByWeather {
    sunny_days_sales: number;
    rainy_days_sales: number;
    sunny_days_count: number;
    rainy_days_count: number;
}

interface DailySale {
    date: string;
    total_sales: number;
    temperature_max?: number;
    temperature_min?: number;
    is_forecast?: boolean;
}

interface Demographics {
    name: string;
    value: number;
}

interface ProductRanking {
    name: string;
    value: number;
}

interface ProductRankings {
    quantity_ranking: ProductRanking[];
    sales_ranking: ProductRanking[];
}

export default function DashboardPage() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [weatherAnalysis, setWeatherAnalysis] = useState<SalesByWeather | null>(null);
    const [dailySales, setDailySales] = useState<DailySale[]>([]);
    const [demographics, setDemographics] = useState<{ age: Demographics[], gender: Demographics[] }>({ age: [], gender: [] });
    const [productRankings, setProductRankings] = useState<ProductRankings>({ quantity_ranking: [], sales_ranking: [] });
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

                const [weatherRes, dailySalesRes, demographicsRes, rankingsRes] = await Promise.all([
                    fetch(`${apiBaseUrl}/api/analysis/sales-by-weather`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/daily-sales?days_back=7&days_forward=7`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/customer-demographics`, { headers: { 'Authorization': `Bearer ${token}` } }),
                    fetch(`${apiBaseUrl}/api/analysis/product-rankings?limit=5`, { headers: { 'Authorization': `Bearer ${token}` } })
                ]);

                if (!weatherRes.ok || !dailySalesRes.ok || !demographicsRes.ok || !rankingsRes.ok) {
                    // Find the first error response to show a more specific message
                    const errorRes = [weatherRes, dailySalesRes, demographicsRes, rankingsRes].find(res => !res.ok);
                    const errorData = errorRes ? await errorRes.json() : { detail: 'データの取得に失敗しました。' };
                    throw new Error(errorData.detail);
                }

                const weatherData: SalesByWeather = await weatherRes.json();
                const dailySalesData: DailySale[] = await dailySalesRes.json();
                const demographicsData = await demographicsRes.json();
                const rankingsData: ProductRankings = await rankingsRes.json();

                setWeatherAnalysis(weatherData);
                setDailySales(dailySalesData.map(d => ({...d, date: new Date(d.date).toLocaleDateString('ja-JP', { month: 'numeric', day: 'numeric' }) })));
                setDemographics({
                    age: demographicsData.age_demographics,
                    gender: demographicsData.gender_demographics
                });
                setProductRankings(rankingsData);

            } catch (err) {
                setError(err instanceof Error ? err.message : '不明なエラーが発生しました。');
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [token]);

    const WeatherSalesCard = () => {
        if (isLoading) return <div className="text-center text-gray-500">分析データを読み込み中...</div>;
        if (error) return <div className="flex items-center text-red-600"><AlertTriangle className="w-6 h-6 mr-2" /><p>{error}</p></div>;
        if (weatherAnalysis) {
            return (
                <>
                    <div className="flex items-center space-x-4">
                        <Sun className="w-12 h-12 text-yellow-500"/>
                        <div>
                            <p className="text-gray-500">晴れの日 ({weatherAnalysis.sunny_days_count}日間) の平均売上</p>
                            <p className="text-2xl font-bold">¥{Math.round(weatherAnalysis.sunny_days_sales).toLocaleString()}</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4 mt-4">
                        <CloudRain className="w-12 h-12 text-blue-500"/>
                        <div>
                            <p className="text-gray-500">雨の日 ({weatherAnalysis.rainy_days_count}日間) の平均売上</p>
                            <p className="text-2xl font-bold">¥{Math.round(weatherAnalysis.rainy_days_sales).toLocaleString()}</p>
                        </div>
                    </div>
                </>
            );
        }
        return <div className="text-center text-gray-500">分析データがありません。</div>;
    };

    const SalesChart = () => {
        if (isLoading) return <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center"><p className="text-gray-400">グラフを読み込み中...</p></div>;
        if (error) return <div className="h-64 bg-red-50 rounded-lg flex items-center justify-center text-red-600"><AlertTriangle className="w-8 h-8 mr-2" /><p>グラフの表示に失敗しました。</p></div>;
        if (dailySales.length > 0) {
            // データをそのまま使用（バックエンドで今日のデータが適切に処理されている）
            const allData = dailySales;

            return (
                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={allData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis yAxisId="sales" orientation="left" />
                        <YAxis yAxisId="temp" orientation="right" />
                        <Tooltip
                            formatter={(value, name) => {
                                const nameStr = String(name);
                                if (nameStr === '売上' || nameStr === '売上（実測）') return [`¥${value?.toLocaleString()}`, name];
                                if (nameStr.includes('気温') || nameStr.includes('予測')) return [`${value}°C`, name];
                                return [value, name];
                            }}
                        />
                        <Legend />
                        {/* 実測データの売上（売上が0でなければ表示） */}
                        <Line
                            yAxisId="sales"
                            type="monotone"
                            dataKey={(d) => d.total_sales > 0 ? d.total_sales : null}
                            name="売上（実測）"
                            stroke="#8884d8"
                            strokeWidth={3}
                            connectNulls={false}
                        />
                        {/* 実測データの気温 */}
                        <Line
                            yAxisId="temp"
                            type="monotone"
                            dataKey={(d) => !d.is_forecast ? d.temperature_max : null}
                            name="最高気温（実測）"
                            stroke="#ff7300"
                            strokeWidth={2}
                            connectNulls={false}
                        />
                        <Line
                            yAxisId="temp"
                            type="monotone"
                            dataKey={(d) => !d.is_forecast ? d.temperature_min : null}
                            name="最低気温（実測）"
                            stroke="#82ca9d"
                            strokeWidth={2}
                            connectNulls={false}
                        />
                        {/* 予測データの気温（点線） */}
                        <Line
                            yAxisId="temp"
                            type="monotone"
                            dataKey={(d) => d.is_forecast ? d.temperature_max : null}
                            name="最高気温（予測）"
                            stroke="#ff7300"
                            strokeWidth={2}
                            strokeDasharray="5 5"
                            connectNulls={true}
                            strokeOpacity={0.6}
                        />
                        <Line
                            yAxisId="temp"
                            type="monotone"
                            dataKey={(d) => d.is_forecast ? d.temperature_min : null}
                            name="最低気温（予測）"
                            stroke="#82ca9d"
                            strokeWidth={2}
                            strokeDasharray="5 5"
                            connectNulls={true}
                            strokeOpacity={0.6}
                        />
                    </LineChart>
                </ResponsiveContainer>
            );
        }
        return <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center"><p className="text-gray-400">売上データがありません。</p></div>;
    }

    const DemographicsChart = ({ data, title }: { data: Demographics[], title: string }) => {
        const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF'];
        if (isLoading) return <div className="h-40 bg-gray-100 rounded-lg flex items-center justify-center"><p className="text-gray-400">グラフを読み込み中...</p></div>;
        if (error) return <div className="h-40 bg-red-50 rounded-lg flex items-center justify-center text-red-600"><AlertTriangle className="w-8 h-8 mr-2" /><p>失敗</p></div>;
        if (data.length > 0) {
            return (
                <div>
                    <h4 className="font-semibold text-center mb-2">{title}</h4>
                    <ResponsiveContainer width="100%" height={150}>
                        <PieChart>
                            <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} fill="#8884d8" label>
                                {data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            );
        }
        return <div className="h-40 bg-gray-100 rounded-lg flex items-center justify-center"><p className="text-gray-400">データがありません。</p></div>;
    }

    return (
        <motion.div
            className="min-h-screen bg-gray-100 py-24"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="container mx-auto px-6">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold">経営ダッシュボード</h1>
                    <Link href="/" className="text-sm text-gray-500 hover:text-gray-700">トップページに戻る</Link>
                </div>

                {/* Quick Actions */}
                <div className="mb-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                        <Link href="/products">
                            <motion.div
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-200"
                            >
                                <div className="flex items-center justify-center mb-2">
                                    <Package className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-center font-semibold text-gray-900">商品管理</h3>
                                <p className="text-center text-sm text-gray-600 mt-1">商品の追加・編集</p>
                            </motion.div>
                        </Link>

                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-200"
                        >
                            <div className="flex items-center justify-center mb-2">
                                <Users className="w-8 h-8 text-green-600" />
                            </div>
                            <h3 className="text-center font-semibold text-gray-900">顧客管理</h3>
                            <p className="text-center text-sm text-gray-600 mt-1">近日公開</p>
                        </motion.div>

                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-200"
                        >
                            <div className="flex items-center justify-center mb-2">
                                <BarChart3 className="w-8 h-8 text-purple-600" />
                            </div>
                            <h3 className="text-center font-semibold text-gray-900">売上分析</h3>
                            <p className="text-center text-sm text-gray-600 mt-1">詳細レポート</p>
                        </motion.div>

                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-200"
                        >
                            <div className="flex items-center justify-center mb-2">
                                <Settings className="w-8 h-8 text-gray-600" />
                            </div>
                            <h3 className="text-center font-semibold text-gray-900">設定</h3>
                            <p className="text-center text-sm text-gray-600 mt-1">店舗情報設定</p>
                        </motion.div>
                    </div>

                    <div className="text-center">
                        <motion.button
                            onClick={() => setIsModalOpen(true)}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-bold py-3 px-6 rounded-full focus:outline-none focus:shadow-outline transition-all shadow-lg hover:shadow-xl flex items-center justify-center mx-auto"
                        >
                            <Sparkles className="w-5 h-5 mr-2"/>
                            AIによる経営アドバイス ✨
                        </motion.button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 space-y-8">
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h3 className="font-bold text-xl mb-4">売上推移と気温予測（過去7日間 + 未来7日間）</h3>
                            <SalesChart />
                        </div>
                        <div className="grid md:grid-cols-2 gap-8">
                            <div className="bg-white p-6 rounded-xl shadow-md">
                                <h3 className="font-bold text-xl mb-4">天気と売上</h3>
                                <WeatherSalesCard />
                            </div>
                            <div className="bg-white p-6 rounded-xl shadow-md">
                                <h3 className="font-bold text-xl mb-4">主な客層</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <DemographicsChart data={demographics.age} title="年代" />
                                    <DemographicsChart data={demographics.gender} title="性別" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow-md">
                        <h3 className="font-bold text-xl mb-6">人気商品ランキング</h3>
                        {isLoading ? (
                            <div className="text-center text-gray-500 py-8">ランキング読み込み中...</div>
                        ) : error ? (
                            <div className="text-center text-red-600 py-8 flex items-center justify-center">
                                <AlertTriangle className="w-6 h-6 mr-2" />
                                <p>データ取得失敗</p>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                <div>
                                    <h4 className="font-semibold text-lg mb-3 text-blue-600">購入数ランキング</h4>
                                    {productRankings.quantity_ranking.length > 0 ? (
                                        <ul className="space-y-3">
                                            {productRankings.quantity_ranking.map((item, index) => (
                                                <li key={index} className="flex items-center justify-between">
                                                    <div className="flex items-center">
                                                        <span className={`text-lg font-bold mr-4 ${
                                                            index === 0 ? 'text-yellow-500' :
                                                            index === 1 ? 'text-gray-400' :
                                                            index === 2 ? 'text-orange-400' : 'text-gray-500'
                                                        }`}>
                                                            {index + 1}.
                                                        </span>
                                                        <span className="text-gray-700">{item.name}</span>
                                                    </div>
                                                    <span className="text-sm text-gray-500">{item.value}個</span>
                                                </li>
                                            ))}
                                        </ul>
                                    ) : (
                                        <p className="text-gray-500 text-sm">データがありません</p>
                                    )}
                                </div>
                                <div className="border-t pt-4">
                                    <h4 className="font-semibold text-lg mb-3 text-green-600">売上ランキング</h4>
                                    {productRankings.sales_ranking.length > 0 ? (
                                        <ul className="space-y-3">
                                            {productRankings.sales_ranking.map((item, index) => (
                                                <li key={index} className="flex items-center justify-between">
                                                    <div className="flex items-center">
                                                        <span className={`text-lg font-bold mr-4 ${
                                                            index === 0 ? 'text-yellow-500' :
                                                            index === 1 ? 'text-gray-400' :
                                                            index === 2 ? 'text-orange-400' : 'text-gray-500'
                                                        }`}>
                                                            {index + 1}.
                                                        </span>
                                                        <span className="text-gray-700">{item.name}</span>
                                                    </div>
                                                    <span className="text-sm text-gray-500">¥{item.value.toLocaleString()}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    ) : (
                                        <p className="text-gray-500 text-sm">データがありません</p>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <AiAdviceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
        </motion.div>
    );
};
