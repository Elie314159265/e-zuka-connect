"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuthStore } from '../../store/authStore';
import { Plus, Search, Package, Tag, AlertTriangle, Edit, Trash2 } from 'lucide-react';
import ProductForm from '../../components/ProductForm';
import CategoryForm from '../../components/CategoryForm';

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

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<ProductCategory[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Modal states
    const [showProductForm, setShowProductForm] = useState(false);
    const [showCategoryForm, setShowCategoryForm] = useState(false);
    const [editingProduct, setEditingProduct] = useState<Product | null>(null);
    const [editingCategory, setEditingCategory] = useState<ProductCategory | null>(null);

    const { token } = useAuthStore();

    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

    // Fetch data
    const fetchProducts = async () => {
        if (!token) return;

        try {
            let url = `${apiBaseUrl}/api/products`;
            const params = new URLSearchParams();
            if (selectedCategory) params.append('category_id', selectedCategory.toString());
            if (params.toString()) url += `?${params.toString()}`;

            const response = await fetch(url, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setProducts(data);
            } else {
                throw new Error('商品の取得に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const fetchCategories = async () => {
        if (!token) return;

        try {
            const response = await fetch(`${apiBaseUrl}/api/products/categories`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setCategories(data);
            } else {
                throw new Error('カテゴリの取得に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const searchProducts = async () => {
        if (!token || !searchQuery.trim()) return fetchProducts();

        try {
            const response = await fetch(`${apiBaseUrl}/api/products/search?q=${encodeURIComponent(searchQuery)}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setProducts(data);
            } else {
                throw new Error('商品の検索に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const deleteProduct = async (productId: number) => {
        if (!token || !confirm('この商品を削除しますか？')) return;

        try {
            const response = await fetch(`${apiBaseUrl}/api/products/${productId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                await fetchProducts();
            } else {
                throw new Error('商品の削除に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    const deleteCategory = async (categoryId: number) => {
        if (!token || !confirm('このカテゴリを削除しますか？')) return;

        try {
            const response = await fetch(`${apiBaseUrl}/api/products/categories/${categoryId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                await fetchCategories();
                await fetchProducts();
            } else {
                throw new Error('カテゴリの削除に失敗しました');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
    };

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            await Promise.all([fetchProducts(), fetchCategories()]);
            setIsLoading(false);
        };

        if (token) {
            loadData();
        }
    }, [token, selectedCategory]);

    useEffect(() => {
        const delayedSearch = setTimeout(() => {
            if (searchQuery) {
                searchProducts();
            } else {
                fetchProducts();
            }
        }, 300);

        return () => clearTimeout(delayedSearch);
    }, [searchQuery]);

    const lowStockProducts = products.filter(p => p.stock_quantity <= p.low_stock_threshold);

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
                                <Package className="text-blue-600" />
                                商品管理
                            </h1>
                            <p className="text-gray-600 mt-1">商品とカテゴリの管理を行います</p>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-3">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setShowCategoryForm(true)}
                                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
                            >
                                <Tag size={20} />
                                カテゴリ追加
                            </motion.button>

                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setShowProductForm(true)}
                                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                            >
                                <Plus size={20} />
                                商品追加
                            </motion.button>
                        </div>
                    </div>
                </div>

                {/* Alert for low stock */}
                {lowStockProducts.length > 0 && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                        <div className="flex items-center gap-2 text-yellow-800">
                            <AlertTriangle size={20} />
                            <h3 className="font-semibold">在庫少警告</h3>
                        </div>
                        <p className="text-yellow-700 mt-1">
                            {lowStockProducts.length}件の商品が在庫少の状態です
                        </p>
                        <div className="mt-2 flex flex-wrap gap-2">
                            {lowStockProducts.slice(0, 3).map(product => (
                                <span key={product.id} className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">
                                    {product.name} (残り{product.stock_quantity}個)
                                </span>
                            ))}
                            {lowStockProducts.length > 3 && (
                                <span className="text-yellow-700 text-sm">他{lowStockProducts.length - 3}件...</span>
                            )}
                        </div>
                    </div>
                )}

                {/* Search and Filter */}
                <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                    <div className="flex flex-col lg:flex-row gap-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                                <input
                                    type="text"
                                    placeholder="商品名、説明、商品コードで検索..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                        </div>

                        <div className="lg:w-64">
                            <select
                                value={selectedCategory || ''}
                                onChange={(e) => setSelectedCategory(e.target.value ? parseInt(e.target.value) : null)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="">全てのカテゴリ</option>
                                {categories.map(category => (
                                    <option key={category.id} value={category.id}>
                                        {category.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>

                {/* Categories Section */}
                <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Tag className="text-green-600" />
                        カテゴリ管理
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {categories.map(category => (
                            <div key={category.id} className="border border-gray-200 rounded-lg p-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="font-semibold text-gray-900">{category.name}</h3>
                                        {category.description && (
                                            <p className="text-gray-600 text-sm mt-1">{category.description}</p>
                                        )}
                                        <span className={`inline-block px-2 py-1 rounded-full text-xs mt-2 ${
                                            category.is_active
                                                ? 'bg-green-100 text-green-800'
                                                : 'bg-gray-100 text-gray-800'
                                        }`}>
                                            {category.is_active ? '有効' : '無効'}
                                        </span>
                                    </div>

                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => {
                                                setEditingCategory(category);
                                                setShowCategoryForm(true);
                                            }}
                                            className="text-blue-600 hover:text-blue-800 p-1"
                                        >
                                            <Edit size={16} />
                                        </button>
                                        <button
                                            onClick={() => deleteCategory(category.id)}
                                            className="text-red-600 hover:text-red-800 p-1"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Products Section */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Package className="text-blue-600" />
                        商品一覧 ({products.length}件)
                    </h2>

                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">商品名</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">カテゴリ</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">価格</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">在庫</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">状態</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {products.map(product => (
                                    <tr key={product.id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-3 px-4">
                                            <div>
                                                <div className="font-medium text-gray-900">{product.name}</div>
                                                {product.product_code && (
                                                    <div className="text-sm text-gray-500">コード: {product.product_code}</div>
                                                )}
                                                {product.description && (
                                                    <div className="text-sm text-gray-600 mt-1">{product.description}</div>
                                                )}
                                            </div>
                                        </td>
                                        <td className="py-3 px-4">
                                            <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-sm">
                                                {product.category?.name || '未分類'}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4 font-medium">¥{product.unit_price.toLocaleString()}</td>
                                        <td className="py-3 px-4">
                                            <span className={`font-medium ${
                                                product.stock_quantity <= product.low_stock_threshold
                                                    ? 'text-red-600'
                                                    : 'text-gray-900'
                                            }`}>
                                                {product.stock_quantity}個
                                            </span>
                                            {product.stock_quantity <= product.low_stock_threshold && (
                                                <div className="text-xs text-red-600 mt-1">在庫少</div>
                                            )}
                                        </td>
                                        <td className="py-3 px-4">
                                            <div className="flex flex-col gap-1">
                                                <span className={`inline-block px-2 py-1 rounded-full text-xs ${
                                                    product.is_active
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-gray-100 text-gray-800'
                                                }`}>
                                                    {product.is_active ? '販売中' : '停止中'}
                                                </span>
                                                {product.is_featured && (
                                                    <span className="inline-block px-2 py-1 rounded-full text-xs bg-yellow-100 text-yellow-800">
                                                        おすすめ
                                                    </span>
                                                )}
                                            </div>
                                        </td>
                                        <td className="py-3 px-4">
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={() => {
                                                        setEditingProduct(product);
                                                        setShowProductForm(true);
                                                    }}
                                                    className="text-blue-600 hover:text-blue-800 p-1"
                                                >
                                                    <Edit size={16} />
                                                </button>
                                                <button
                                                    onClick={() => deleteProduct(product.id)}
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

                        {products.length === 0 && (
                            <div className="text-center py-8 text-gray-500">
                                商品が見つかりませんでした
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

                {/* Modals */}
                {showProductForm && (
                    <ProductForm
                        product={editingProduct}
                        categories={categories}
                        onClose={() => {
                            setShowProductForm(false);
                            setEditingProduct(null);
                        }}
                        onSave={() => {
                            fetchProducts();
                            setShowProductForm(false);
                            setEditingProduct(null);
                        }}
                    />
                )}

                {showCategoryForm && (
                    <CategoryForm
                        category={editingCategory}
                        onClose={() => {
                            setShowCategoryForm(false);
                            setEditingCategory(null);
                        }}
                        onSave={() => {
                            fetchCategories();
                            setShowCategoryForm(false);
                            setEditingCategory(null);
                        }}
                    />
                )}
            </div>
        </motion.div>
    );
}