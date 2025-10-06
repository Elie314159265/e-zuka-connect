"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuthStore } from '../../store/authStore';
import { Plus, Search, Megaphone, Edit, Trash2, Calendar, Eye } from 'lucide-react';
import PromotionForm from '../../components/PromotionForm';

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
}

interface Promotion {
    id: number;
    title: string;
    description?: string;
    promotion_text?: string;
    promotion_image_urls?: string[];
    start_date: string;
    end_date: string;
    status: string;
    is_auto_published: boolean;
    published_at?: string;
    display_priority: number;
    current_views: number;
    product: Product;
}

export default function PromotionsPage() {
    const [promotions, setPromotions] = useState<Promotion[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [statusFilter, setStatusFilter] = useState<string>('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Modal states
    const [showPromotionForm, setShowPromotionForm] = useState(false);
    const [editingPromotion, setEditingPromotion] = useState<Promotion | null>(null);

    const { token } = useAuthStore();

    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

    // Fetch promotions
    const fetchPromotions = async () => {
        if (!token) return;

        try {
            let url = `${apiBaseUrl}/api/promotions/`;
            const params = new URLSearchParams();
            if (statusFilter) params.append('status', statusFilter);
            if (params.toString()) url += `?${params.toString()}`;

            const response = await fetch(url, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setPromotions(data);
            } else {
                throw new Error('プロモーションの取得に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const deletePromotion = async (promotionId: number) => {
        if (!token || !confirm('このプロモーションを削除しますか？')) return;

        try {
            const response = await fetch(`${apiBaseUrl}/api/promotions/${promotionId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                await fetchPromotions();
            } else {
                throw new Error('プロモーションの削除に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const publishPromotion = async (promotionId: number) => {
        if (!token) return;

        try {
            const response = await fetch(`${apiBaseUrl}/api/promotions/${promotionId}/publish`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                await fetchPromotions();
            } else {
                throw new Error('プロモーションの公開に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            await fetchPromotions();
            setIsLoading(false);
        };

        if (token) {
            loadData();
        }
    }, [token, statusFilter]);

    const filteredPromotions = promotions.filter(promo =>
        promo.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        promo.product.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const getStatusBadge = (status: string) => {
        const statusConfig = {
            draft: { label: '下書き', color: 'bg-gray-100 text-gray-800' },
            scheduled: { label: '予定', color: 'bg-blue-100 text-blue-800' },
            active: { label: '公開中', color: 'bg-green-100 text-green-800' },
            expired: { label: '期限切れ', color: 'bg-red-100 text-red-800' },
            paused: { label: '一時停止', color: 'bg-yellow-100 text-yellow-800' }
        };

        const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.draft;
        return <span className={`inline-block px-2 py-1 rounded-full text-xs ${config.color}`}>{config.label}</span>;
    };

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

    return (
        <motion.div
            className="min-h-screen bg-gray-50 py-8 px-4"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
                                <Megaphone className="text-blue-600" />
                                プロモーション管理
                            </h1>
                            <p className="text-gray-600 mt-1">商品のプロモーションを作成・管理します</p>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setShowPromotionForm(true)}
                            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                        >
                            <Plus size={20} />
                            プロモーション追加
                        </motion.button>
                    </div>
                </div>

                {/* Search and Filter */}
                <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                    <div className="flex flex-col lg:flex-row gap-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                                <input
                                    type="text"
                                    placeholder="プロモーションタイトル、商品名で検索..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                        </div>

                        <div className="lg:w-64">
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="">全てのステータス</option>
                                <option value="draft">下書き</option>
                                <option value="scheduled">予定</option>
                                <option value="active">公開中</option>
                                <option value="expired">期限切れ</option>
                                <option value="paused">一時停止</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Promotions List */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        プロモーション一覧 ({filteredPromotions.length}件)
                    </h2>

                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">タイトル</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">商品</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">期間</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">ステータス</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">閲覧数</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPromotions.map(promotion => (
                                    <tr key={promotion.id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-3 px-4">
                                            <div>
                                                <div className="font-medium text-gray-900">{promotion.title}</div>
                                                {promotion.description && (
                                                    <div className="text-sm text-gray-600 mt-1">{promotion.description}</div>
                                                )}
                                            </div>
                                        </td>
                                        <td className="py-3 px-4">
                                            <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-sm">
                                                {promotion.product.name}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4">
                                            <div className="text-sm">
                                                <div className="flex items-center gap-1">
                                                    <Calendar size={14} />
                                                    <span>{new Date(promotion.start_date).toLocaleDateString('ja-JP')}</span>
                                                </div>
                                                <div className="text-gray-500">
                                                    〜 {new Date(promotion.end_date).toLocaleDateString('ja-JP')}
                                                </div>
                                            </div>
                                        </td>
                                        <td className="py-3 px-4">
                                            {getStatusBadge(promotion.status)}
                                        </td>
                                        <td className="py-3 px-4">
                                            <div className="flex items-center gap-1">
                                                <Eye size={16} className="text-gray-400" />
                                                <span className="font-medium">{promotion.current_views}</span>
                                            </div>
                                        </td>
                                        <td className="py-3 px-4">
                                            <div className="flex gap-2">
                                                {promotion.status === 'scheduled' && (
                                                    <button
                                                        onClick={() => publishPromotion(promotion.id)}
                                                        className="text-green-600 hover:text-green-800 p-1 text-xs bg-green-50 px-2 rounded"
                                                    >
                                                        公開
                                                    </button>
                                                )}
                                                <button
                                                    onClick={() => {
                                                        setEditingPromotion(promotion);
                                                        setShowPromotionForm(true);
                                                    }}
                                                    className="text-blue-600 hover:text-blue-800 p-1"
                                                >
                                                    <Edit size={16} />
                                                </button>
                                                <button
                                                    onClick={() => deletePromotion(promotion.id)}
                                                    className="text-red-600 hover:text-red-800 p-1"
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {filteredPromotions.length === 0 && (
                            <div className="text-center py-8 text-gray-500">
                                プロモーションが見つかりませんでした
                            </div>
                        )}
                    </div>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50">
                        {error}
                        <button
                            onClick={() => setError(null)}
                            className="ml-2 text-red-500 hover:text-red-700"
                        >
                            ×
                        </button>
                    </div>
                )}

                {/* Modal */}
                {showPromotionForm && (
                    <PromotionForm
                        promotion={editingPromotion}
                        onClose={() => {
                            setShowPromotionForm(false);
                            setEditingPromotion(null);
                        }}
                        onSave={() => {
                            fetchPromotions();
                            setShowPromotionForm(false);
                            setEditingPromotion(null);
                        }}
                    />
                )}
            </div>
        </motion.div>
    );
}
