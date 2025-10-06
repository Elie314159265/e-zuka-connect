"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuthStore } from '../store/authStore';
import { X } from 'lucide-react';

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
    display_priority: number;
    product: Product;
    product_id?: number;
}

interface PromotionFormProps {
    promotion: Promotion | null;
    onClose: () => void;
    onSave: () => void;
}

export default function PromotionForm({ promotion, onClose, onSave }: PromotionFormProps) {
    const [products, setProducts] = useState<Product[]>([]);
    const [formData, setFormData] = useState({
        product_id: promotion?.product_id || promotion?.product?.id || 0,
        title: promotion?.title || '',
        description: promotion?.description || '',
        promotion_text: promotion?.promotion_text || '',
        promotion_image_urls: promotion?.promotion_image_urls || [],
        start_date: promotion?.start_date ? new Date(promotion.start_date).toISOString().slice(0, 16) : '',
        end_date: promotion?.end_date ? new Date(promotion.end_date).toISOString().slice(0, 16) : '',
        is_auto_published: promotion?.is_auto_published ?? true,
        display_priority: promotion?.display_priority || 0
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const { token } = useAuthStore();
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

    useEffect(() => {
        const fetchProducts = async () => {
            if (!token) return;

            try {
                const response = await fetch(`${apiBaseUrl}/api/products/`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();
                    setProducts(data);
                }
            } catch (err) {
                console.error('Failed to fetch products:', err);
            }
        };

        fetchProducts();
    }, [token, apiBaseUrl]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const url = promotion
                ? `${apiBaseUrl}/api/promotions/${promotion.id}`
                : `${apiBaseUrl}/api/promotions/`;

            const method = promotion ? 'PUT' : 'POST';

            const payload = {
                ...formData,
                product_id: parseInt(formData.product_id.toString()),
                start_date: new Date(formData.start_date).toISOString(),
                end_date: new Date(formData.end_date).toISOString(),
                display_priority: parseInt(formData.display_priority.toString())
            };

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                onSave();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'プロモーションの保存に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
                <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-gray-900">
                        {promotion ? 'プロモーション編集' : 'プロモーション追加'}
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600"
                    >
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    {error && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            商品 <span className="text-red-500">*</span>
                        </label>
                        <select
                            value={formData.product_id}
                            onChange={(e) => setFormData({ ...formData, product_id: parseInt(e.target.value) })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                        >
                            <option value={0}>商品を選択してください</option>
                            {products.map(product => (
                                <option key={product.id} value={product.id}>
                                    {product.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            タイトル <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                            placeholder="例: 秋の大感謝セール"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            説明
                        </label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            rows={3}
                            placeholder="プロモーションの概要を入力してください"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            プロモーション本文
                        </label>
                        <textarea
                            value={formData.promotion_text}
                            onChange={(e) => setFormData({ ...formData, promotion_text: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            rows={5}
                            placeholder="プロモーションの詳細な内容を入力してください"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                開始日時 <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="datetime-local"
                                value={formData.start_date}
                                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                終了日時 <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="datetime-local"
                                value={formData.end_date}
                                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            表示優先度
                        </label>
                        <input
                            type="number"
                            value={formData.display_priority}
                            onChange={(e) => setFormData({ ...formData, display_priority: parseInt(e.target.value) || 0 })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="数値が大きいほど優先的に表示されます"
                        />
                        <p className="text-sm text-gray-500 mt-1">
                            数値が大きいほど優先的に表示されます（デフォルト: 0）
                        </p>
                    </div>

                    <div className="flex items-center">
                        <input
                            type="checkbox"
                            id="is_auto_published"
                            checked={formData.is_auto_published}
                            onChange={(e) => setFormData({ ...formData, is_auto_published: e.target.checked })}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <label htmlFor="is_auto_published" className="ml-2 block text-sm text-gray-900">
                            自動掲載を有効にする（開始日時になったら自動的に公開）
                        </label>
                    </div>

                    <div className="flex gap-3 pt-4 border-t border-gray-200">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                        >
                            キャンセル
                        </button>
                        <button
                            type="submit"
                            disabled={loading || formData.product_id === 0}
                            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                        >
                            {loading ? '保存中...' : (promotion ? '更新' : '作成')}
                        </button>
                    </div>
                </form>
            </motion.div>
        </div>
    );
}
