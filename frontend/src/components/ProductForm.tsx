"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { X, Save, Package, DollarSign, Hash, FileText } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

interface Product {
    id: number;
    name: string;
    description?: string;
    unit_price: number;
    cost_price?: number;
    stock_quantity: number;
    low_stock_threshold: number;
    is_active: boolean;
    is_featured: boolean;
    is_seasonal: boolean;
    category?: ProductCategory;
    product_code?: string;
    unit: string;
    tax_rate: number;
}

interface ProductCategory {
    id: number;
    name: string;
    description?: string;
    is_active: boolean;
}

interface ProductFormProps {
    product?: Product | null;
    categories: ProductCategory[];
    onClose: () => void;
    onSave: () => void;
}

export default function ProductForm({ product, categories, onClose, onSave }: ProductFormProps) {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        category_id: '',
        product_code: '',
        unit_price: '',
        cost_price: '',
        tax_rate: '0.10',
        unit: '個',
        stock_quantity: '',
        low_stock_threshold: '10',
        is_active: true,
        is_featured: false,
        is_seasonal: false
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const { token } = useAuthStore();
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

    useEffect(() => {
        if (product) {
            setFormData({
                name: product.name,
                description: product.description || '',
                category_id: product.category?.id.toString() || '',
                product_code: product.product_code || '',
                unit_price: product.unit_price.toString(),
                cost_price: product.cost_price?.toString() || '',
                tax_rate: product.tax_rate.toString(),
                unit: product.unit,
                stock_quantity: product.stock_quantity.toString(),
                low_stock_threshold: product.low_stock_threshold.toString(),
                is_active: product.is_active,
                is_featured: product.is_featured,
                is_seasonal: product.is_seasonal
            });
        }
    }, [product]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);

        try {
            // バリデーション
            if (!formData.name.trim()) {
                throw new Error('商品名は必須です');
            }
            if (!formData.unit_price || isNaN(Number(formData.unit_price)) || Number(formData.unit_price) <= 0) {
                throw new Error('有効な価格を入力してください');
            }

            const submitData = {
                name: formData.name.trim(),
                description: formData.description.trim() || null,
                category_id: formData.category_id ? parseInt(formData.category_id) : null,
                product_code: formData.product_code.trim() || null,
                unit_price: parseInt(formData.unit_price),
                cost_price: formData.cost_price ? parseInt(formData.cost_price) : null,
                tax_rate: parseFloat(formData.tax_rate),
                unit: formData.unit,
                stock_quantity: parseInt(formData.stock_quantity) || 0,
                low_stock_threshold: parseInt(formData.low_stock_threshold) || 10,
                is_active: formData.is_active,
                is_featured: formData.is_featured,
                is_seasonal: formData.is_seasonal
            };

            const url = product
                ? `${apiBaseUrl}/api/products/${product.id}`
                : `${apiBaseUrl}/api/products`;

            const method = product ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(submitData)
            });

            if (response.ok) {
                onSave();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || '商品の保存に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        } finally {
            setIsLoading(false);
        }
    };

    const unitOptions = ['個', 'kg', 'g', 'L', 'ml', '本', '袋', '箱', 'パック'];

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-screen overflow-y-auto"
            >
                <div className="flex items-center justify-between p-6 border-b">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                        <Package className="text-blue-600" />
                        {product ? '商品編集' : '新規商品登録'}
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6">
                    {error && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-6">
                            <p className="text-red-700 text-sm">{error}</p>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* 基本情報 */}
                        <div className="md:col-span-2">
                            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center gap-2">
                                <FileText className="text-blue-600" size={20} />
                                基本情報
                            </h3>
                        </div>

                        <div className="md:col-span-2">
                            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                                商品名 <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="例: 青森産りんご"
                                required
                            />
                        </div>

                        <div className="md:col-span-2">
                            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                                商品説明
                            </label>
                            <textarea
                                id="description"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                rows={3}
                                placeholder="商品の詳細説明を入力してください"
                            />
                        </div>

                        <div>
                            <label htmlFor="category_id" className="block text-sm font-medium text-gray-700 mb-1">
                                カテゴリ
                            </label>
                            <select
                                id="category_id"
                                value={formData.category_id}
                                onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="">未分類</option>
                                {categories.filter(cat => cat.is_active).map(category => (
                                    <option key={category.id} value={category.id}>
                                        {category.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label htmlFor="product_code" className="block text-sm font-medium text-gray-700 mb-1">
                                商品コード
                            </label>
                            <input
                                type="text"
                                id="product_code"
                                value={formData.product_code}
                                onChange={(e) => setFormData({ ...formData, product_code: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="例: APPLE001"
                            />
                        </div>

                        {/* 価格設定 */}
                        <div className="md:col-span-2 mt-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center gap-2">
                                <DollarSign className="text-green-600" size={20} />
                                価格設定
                            </h3>
                        </div>

                        <div>
                            <label htmlFor="unit_price" className="block text-sm font-medium text-gray-700 mb-1">
                                販売価格 <span className="text-red-500">*</span>
                            </label>
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">¥</span>
                                <input
                                    type="number"
                                    id="unit_price"
                                    value={formData.unit_price}
                                    onChange={(e) => setFormData({ ...formData, unit_price: e.target.value })}
                                    className="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="150"
                                    min="0"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="cost_price" className="block text-sm font-medium text-gray-700 mb-1">
                                原価
                            </label>
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">¥</span>
                                <input
                                    type="number"
                                    id="cost_price"
                                    value={formData.cost_price}
                                    onChange={(e) => setFormData({ ...formData, cost_price: e.target.value })}
                                    className="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="100"
                                    min="0"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="tax_rate" className="block text-sm font-medium text-gray-700 mb-1">
                                消費税率
                            </label>
                            <select
                                id="tax_rate"
                                value={formData.tax_rate}
                                onChange={(e) => setFormData({ ...formData, tax_rate: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="0.08">8%</option>
                                <option value="0.10">10%</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="unit" className="block text-sm font-medium text-gray-700 mb-1">
                                単位
                            </label>
                            <select
                                id="unit"
                                value={formData.unit}
                                onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                {unitOptions.map(unit => (
                                    <option key={unit} value={unit}>{unit}</option>
                                ))}
                            </select>
                        </div>

                        {/* 在庫管理 */}
                        <div className="md:col-span-2 mt-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center gap-2">
                                <Hash className="text-purple-600" size={20} />
                                在庫管理
                            </h3>
                        </div>

                        <div>
                            <label htmlFor="stock_quantity" className="block text-sm font-medium text-gray-700 mb-1">
                                現在の在庫数
                            </label>
                            <input
                                type="number"
                                id="stock_quantity"
                                value={formData.stock_quantity}
                                onChange={(e) => setFormData({ ...formData, stock_quantity: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="100"
                                min="0"
                            />
                        </div>

                        <div>
                            <label htmlFor="low_stock_threshold" className="block text-sm font-medium text-gray-700 mb-1">
                                在庫少警告閾値
                            </label>
                            <input
                                type="number"
                                id="low_stock_threshold"
                                value={formData.low_stock_threshold}
                                onChange={(e) => setFormData({ ...formData, low_stock_threshold: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="10"
                                min="0"
                            />
                        </div>

                        {/* 商品設定 */}
                        <div className="md:col-span-2 mt-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-4">商品設定</h3>
                            <div className="space-y-3">
                                <div className="flex items-center">
                                    <input
                                        type="checkbox"
                                        id="is_active"
                                        checked={formData.is_active}
                                        onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <label htmlFor="is_active" className="ml-2 text-sm text-gray-700">
                                        販売中（有効にすると顧客に表示されます）
                                    </label>
                                </div>

                                <div className="flex items-center">
                                    <input
                                        type="checkbox"
                                        id="is_featured"
                                        checked={formData.is_featured}
                                        onChange={(e) => setFormData({ ...formData, is_featured: e.target.checked })}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <label htmlFor="is_featured" className="ml-2 text-sm text-gray-700">
                                        おすすめ商品として表示
                                    </label>
                                </div>

                                <div className="flex items-center">
                                    <input
                                        type="checkbox"
                                        id="is_seasonal"
                                        checked={formData.is_seasonal}
                                        onChange={(e) => setFormData({ ...formData, is_seasonal: e.target.checked })}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <label htmlFor="is_seasonal" className="ml-2 text-sm text-gray-700">
                                        季節商品
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-3 mt-8 pt-6 border-t">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            キャンセル
                        </button>
                        <motion.button
                            type="submit"
                            disabled={isLoading}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            <Save size={20} />
                            {isLoading ? '保存中...' : '保存'}
                        </motion.button>
                    </div>
                </form>
            </motion.div>
        </div>
    );
}