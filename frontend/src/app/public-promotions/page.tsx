"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Megaphone, Calendar, Eye, Store } from 'lucide-react';

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

interface Product {
    id: number;
    name: string;
    description?: string;
    unit_price: number;
}

interface Store {
    id: number;
    name: string;
    address?: string;
}

interface Promotion {
    id: number;
    title: string;
    description?: string;
    promotion_text?: string;
    promotion_image_urls?: string[];
    start_date: string;
    end_date: string;
    display_priority: number;
    current_views: number;
    product: Product;
    store?: Store;
}

export default function PublicPromotionsPage() {
    const [promotions, setPromotions] = useState<Promotion[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

    useEffect(() => {
        const fetchPromotions = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(`${apiBaseUrl}/api/promotions/public/active?limit=20`);

                if (response.ok) {
                    const data = await response.json();
                    setPromotions(data);
                } else {
                    throw new Error('プロモーションの取得に失敗しました');
                }
            } catch (err) {
                setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
            } finally {
                setIsLoading(false);
            }
        };

        fetchPromotions();
    }, [apiBaseUrl]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">読み込み中...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-red-600">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <motion.div
            className="min-h-screen bg-gray-50 py-8 px-4"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.5 }}
                        className="inline-flex items-center justify-center w-20 h-20 bg-blue-600 rounded-full mb-4"
                    >
                        <Megaphone size={40} className="text-white" />
                    </motion.div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        本日のプロモーション
                    </h1>
                    <p className="text-xl text-gray-600">
                        地域のお店からのお得な情報をチェック！
                    </p>
                </div>

                {/* Promotions Grid */}
                {promotions.length === 0 ? (
                    <div className="text-center py-16">
                        <div className="text-gray-400 mb-4">
                            <Megaphone size={80} className="mx-auto" />
                        </div>
                        <h2 className="text-2xl font-semibold text-gray-700 mb-2">
                            現在、公開中のプロモーションはありません
                        </h2>
                        <p className="text-gray-500">
                            また後でチェックしてください！
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {promotions.map((promotion, index) => (
                            <motion.div
                                key={promotion.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                            >
                                {/* Promotion Image */}
                                {promotion.promotion_image_urls && promotion.promotion_image_urls.length > 0 ? (
                                    <div className="h-48 bg-gradient-to-r from-blue-400 to-purple-500 relative">
                                        <img
                                            src={promotion.promotion_image_urls[0]}
                                            alt={promotion.title}
                                            className="w-full h-full object-cover"
                                        />
                                    </div>
                                ) : (
                                    <div className="h-48 bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center">
                                        <Megaphone size={60} className="text-white opacity-50" />
                                    </div>
                                )}

                                {/* Promotion Content */}
                                <div className="p-6">
                                    <div className="flex items-start justify-between mb-3">
                                        <h2 className="text-xl font-bold text-gray-900 flex-1">
                                            {promotion.title}
                                        </h2>
                                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full ml-2">
                                            NEW
                                        </span>
                                    </div>

                                    <p className="text-gray-600 mb-4">
                                        {promotion.description || promotion.promotion_text?.slice(0, 100) + '...' || '詳細情報はありません'}
                                    </p>

                                    <div className="space-y-2 mb-4">
                                        <div className="flex items-center text-sm text-gray-500">
                                            <Store size={16} className="mr-2" />
                                            <span className="font-medium text-gray-700">
                                                {promotion.product.name}
                                            </span>
                                        </div>

                                        <div className="flex items-center text-sm text-gray-500">
                                            <Calendar size={16} className="mr-2" />
                                            <span>
                                                {new Date(promotion.start_date).toLocaleDateString('ja-JP')} 〜 {new Date(promotion.end_date).toLocaleDateString('ja-JP')}
                                            </span>
                                        </div>

                                        <div className="flex items-center text-sm text-gray-500">
                                            <Eye size={16} className="mr-2" />
                                            <span>{promotion.current_views} 回閲覧</span>
                                        </div>
                                    </div>

                                    {promotion.promotion_text && (
                                        <div className="border-t border-gray-200 pt-4">
                                            <p className="text-sm text-gray-700 line-clamp-3">
                                                {promotion.promotion_text}
                                            </p>
                                        </div>
                                    )}

                                    <div className="mt-4">
                                        <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
                                            詳細を見る
                                        </button>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}

                {/* Footer Info */}
                <div className="mt-12 text-center text-gray-500 text-sm">
                    <p>プロモーション情報は毎日更新されます</p>
                </div>
            </div>
        </motion.div>
    );
}
