"use client";
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Award, Cake, Star, Lock, UploadCloud, Gift, Megaphone } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useRouter } from 'next/navigation';

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

interface GamificationProfile {
    id: number;
    user_id: number;
    contribution_points: number;
    total_earned_points: number;
    level: number;
}

interface UserBadge {
    id: number;
    profile_id: number;
    badge_id: number;
    awarded_at: string;
    badge: {
        id: number;
        name: string;
        description: string;
        icon_url: string;
    };
}

interface Reward {
    id: number;
    title: string;
    description: string;
    required_points: number;
    reward_type: string;
    is_active: boolean;
    is_featured: boolean;
    available_stock: number | null;
}

export default function MyPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState<string>('');
    const [gamificationProfile, setGamificationProfile] = useState<GamificationProfile | null>(null);
    const [userBadges, setUserBadges] = useState<UserBadge[]>([]);
    const [availableRewards, setAvailableRewards] = useState<Reward[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const { token, isLoggedIn } = useAuthStore();
    const router = useRouter();

    useEffect(() => {
        if (!isLoggedIn()) {
            router.push('/login/user');
            return;
        }
        fetchGamificationData();
    }, [isLoggedIn, router, token]);

    const fetchGamificationData = async () => {
        if (!token) return;
        
        const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
        
        try {
            setIsLoading(true);
            
            // Fetch gamification profile
            const profileResponse = await fetch(`${apiBaseUrl}/api/gamification/profile`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (profileResponse.ok) {
                const profile = await profileResponse.json();
                setGamificationProfile(profile);
            }
            
            // Fetch user badges
            const badgesResponse = await fetch(`${apiBaseUrl}/api/gamification/badges`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (badgesResponse.ok) {
                const badges = await badgesResponse.json();
                setUserBadges(badges);
            }
            
            // Fetch available rewards
            const rewardsResponse = await fetch(`${apiBaseUrl}/api/gamification/rewards`);
            
            if (rewardsResponse.ok) {
                const rewards = await rewardsResponse.json();
                setAvailableRewards(rewards);
            }
            
        } catch (error) {
            console.error('Failed to fetch gamification data:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            const file = event.target.files[0];
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
            setUploadStatus('idle');
            setMessage('');
        }
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!selectedFile) {
            setMessage('ファイルを選択してください。');
            setUploadStatus('error');
            return;
        }
        if (!token) {
            setMessage('認証トークンがありません。再度ログインしてください。');
            setUploadStatus('error');
            return;
        }

        setUploadStatus('uploading');
        setMessage('アップロード中...');

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
            const response = await fetch(`${apiBaseUrl}/api/receipts/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (response.status === 401) {
                setMessage('認証の有効期限が切れました。再度ログインしてください。');
                setUploadStatus('error');
                useAuthStore.getState().setToken(null); // Clear token
                router.push('/login/user');
                return;
            }

            const result = await response.json();

            if (response.ok) {
                setUploadStatus('success');
                const supplierName = result.receipt?.supplier_name || '店舗名不明';
                const totalAmount = result.receipt?.total_amount || '金額不明';
                const pointsEarned = result.points_earned || 0;
                const badgesAwarded = result.badges_awarded || [];
                
                let successMessage = `アップロード成功！ ${supplierName} で ${totalAmount} 円分の貢献を記録しました！`;
                if (pointsEarned > 0) {
                    successMessage += ` ${pointsEarned}ポイント獲得！`;
                }
                if (badgesAwarded.length > 0) {
                    successMessage += ` 新しいバッジを獲得: ${badgesAwarded.map((b: any) => b.badge_name).join(', ')}`;
                }
                
                setMessage(successMessage);
                
                // Refresh gamification data after successful upload
                setTimeout(() => {
                    fetchGamificationData();
                    setSelectedFile(null);
                    setPreviewUrl(null);
                }, 1000);
            } else {
                setUploadStatus('error');
                setMessage(`アップロード失敗: ${result.detail || '不明なエラーが発生しました。'}`);
            }
        } catch (error) {
            setUploadStatus('error');
            setMessage(`クライアントサイドエラー: ${error instanceof Error ? error.message : String(error)}`);
        }
    };

    const handleRewardRedeem = async (rewardId: number) => {
        if (!token) return;
        
        const confirmed = window.confirm('この特典を交換しますか？');
        if (!confirmed) return;
        
        const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
        
        try {
            const response = await fetch(`${apiBaseUrl}/api/gamification/redeem`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ reward_id: rewardId })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                alert(`特典交換完了！クーポンコード: ${result.coupon_code}\n有効期限: ${new Date(result.expires_at).toLocaleDateString()}`);
                // Refresh data to show updated points
                fetchGamificationData();
            } else {
                alert(`交換に失敗しました: ${result.detail}`);
            }
        } catch (error) {
            alert('交換中にエラーが発生しました');
        }
    };

    return (
        <motion.div
            className="min-h-screen bg-gray-100 py-24"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="container mx-auto px-6">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold">マイページ</h1>
                    <Link href="/" className="text-sm text-gray-500 hover:text-gray-700">トップページに戻る</Link>
                </div>
                <div className="bg-white p-8 rounded-xl shadow-md text-center mb-8">
                    <p className="text-gray-500">現在の貢献ポイント</p>
                    {isLoading ? (
                        <div className="animate-pulse">
                            <div className="h-16 bg-gray-200 rounded my-2"></div>
                            <div className="h-4 bg-gray-200 rounded"></div>
                        </div>
                    ) : (
                        <>
                            <p className="text-5xl font-bold text-blue-600 my-2">
                                {gamificationProfile?.contribution_points || 0} <span className="text-2xl">pt</span>
                            </p>
                            <p className="text-gray-600">
                                レベル {gamificationProfile?.level || 1} | 総獲得ポイント {gamificationProfile?.total_earned_points || 0} pt
                            </p>
                            {availableRewards.length > 0 && gamificationProfile && (() => {
                                const nextRewards = availableRewards.filter(r => r.required_points > gamificationProfile.contribution_points);
                                if (nextRewards.length > 0) {
                                    const pointsToNext = Math.min(...nextRewards.map(r => r.required_points - gamificationProfile.contribution_points));
                                    return (
                                        <p className="text-gray-600 mt-2">
                                            次の特典まであと{' '}
                                            <span className="font-bold">{pointsToNext} pt</span>
                                        </p>
                                    );
                                }
                                return null;
                            })()}
                        </>
                    )}
                </div>

                {/* Quick Actions */}
                <div className="mb-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Link href="/public-promotions">
                            <motion.div
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-orange-200"
                            >
                                <div className="flex items-center justify-center mb-2">
                                    <Megaphone className="w-8 h-8 text-orange-600" />
                                </div>
                                <h3 className="text-center font-semibold text-gray-900">今日のプロモーション</h3>
                                <p className="text-center text-sm text-gray-600 mt-1">お得なキャンペーン情報</p>
                            </motion.div>
                        </Link>

                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-200"
                        >
                            <div className="flex items-center justify-center mb-2">
                                <Gift className="w-8 h-8 text-purple-600" />
                            </div>
                            <h3 className="text-center font-semibold text-gray-900">マイクーポン</h3>
                            <p className="text-center text-sm text-gray-600 mt-1">近日公開</p>
                        </motion.div>
                    </div>
                </div>

                {/* File Upload Section */}
                <div className="bg-white p-6 rounded-xl shadow-md mb-8">
                    <h3 className="font-bold text-xl mb-4">レシートを投稿して貢献！</h3>
                    <form onSubmit={handleSubmit}>
                        <div className="flex flex-col sm:flex-row items-center sm:space-x-4">
                            <input
                                type="file"
                                onChange={handleFileChange}
                                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100 mb-4 sm:mb-0"
                                accept="image/png, image/jpeg, image/jpg"
                            />
                            <motion.button
                                type="submit"
                                disabled={!selectedFile || uploadStatus === 'uploading'}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="w-full sm:w-auto flex items-center justify-center px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-full disabled:bg-gray-400 transition-colors"
                            >
                                <UploadCloud className="w-5 h-5 mr-2"/>
                                {uploadStatus === 'uploading' ? '処理中...' : '投稿する'}
                            </motion.button>
                        </div>
                    </form>
                    {previewUrl && (
                        <div className="mt-4">
                            <p className="text-sm text-gray-600">プレビュー:</p>
                            <img src={previewUrl} alt="選択された画像のプレビュー" className="mt-2 max-h-48 rounded-lg shadow-md border" />
                        </div>
                    )}
                    {message && (
                        <div className={`mt-4 p-4 rounded-lg text-sm ${
                            uploadStatus === 'success' ? 'bg-green-100 text-green-800' : ''
                        } ${
                            uploadStatus === 'error' ? 'bg-red-100 text-red-800' : ''
                        } ${
                            uploadStatus === 'uploading' ? 'bg-blue-100 text-blue-800' : ''
                        }`}>
                            <p>{message}</p>
                        </div>
                    )}
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                    <div className="bg-white p-6 rounded-xl shadow-md">
                        <h3 className="font-bold text-xl mb-4">獲得したバッジ</h3>
                        {isLoading ? (
                            <div className="flex flex-wrap gap-4">
                                {[...Array(4)].map((_, i) => (
                                    <div key={i} className="animate-pulse">
                                        <div className="w-16 h-16 bg-gray-200 rounded-full mb-1"></div>
                                        <div className="w-12 h-3 bg-gray-200 rounded"></div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="flex flex-wrap gap-4">
                                {userBadges.length > 0 ? (
                                    userBadges.map((userBadge) => (
                                        <div key={userBadge.id} className="text-center" title={userBadge.badge.description}>
                                            {userBadge.badge.icon_url ? (
                                                <img 
                                                    src={userBadge.badge.icon_url} 
                                                    alt={userBadge.badge.name}
                                                    className="w-16 h-16 mx-auto"
                                                />
                                            ) : (
                                                <Award className="w-16 h-16 text-yellow-500 mx-auto"/>
                                            )}
                                            <span className="text-xs text-gray-500 block mt-1">{userBadge.badge.name}</span>
                                        </div>
                                    ))
                                ) : (
                                    <div className="text-center text-gray-500 w-full">
                                        <Lock className="w-16 h-16 text-gray-300 mx-auto mb-2"/>
                                        <p>まだバッジを獲得していません</p>
                                        <p className="text-sm">レシートをアップロードしてバッジを獲得しよう！</p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow-md">
                        <h3 className="font-bold text-xl mb-4">交換できる特典</h3>
                        {isLoading ? (
                            <ul className="space-y-3">
                                {[...Array(3)].map((_, i) => (
                                    <li key={i} className="animate-pulse">
                                        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                            <div className="h-4 bg-gray-200 rounded w-32"></div>
                                            <div className="h-4 bg-gray-200 rounded w-16"></div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <ul className="space-y-3">
                                {availableRewards.length > 0 ? (
                                    availableRewards.map((reward) => {
                                        const canRedeem = gamificationProfile && gamificationProfile.contribution_points >= reward.required_points;
                                        const isOutOfStock = reward.available_stock !== null && reward.available_stock <= 0;
                                        
                                        return (
                                            <li key={reward.id} 
                                                className={`flex justify-between items-center p-3 rounded-lg ${
                                                    canRedeem && !isOutOfStock 
                                                        ? 'bg-green-50 border border-green-200' 
                                                        : isOutOfStock 
                                                        ? 'bg-red-50 border border-red-200 text-red-600'
                                                        : 'bg-gray-50'
                                                }`}
                                            >
                                                <div className="flex-1">
                                                    <span className="block font-medium">{reward.title}</span>
                                                    <span className="text-sm text-gray-600">{reward.description}</span>
                                                    {reward.available_stock !== null && (
                                                        <span className="text-xs text-gray-500 block">
                                                            在庫: {reward.available_stock}個
                                                        </span>
                                                    )}
                                                </div>
                                                <div className="flex items-center space-x-2">
                                                    {reward.is_featured && (
                                                        <Star className="w-4 h-4 text-yellow-500"/>
                                                    )}
                                                    <span className={`font-bold ${
                                                        canRedeem && !isOutOfStock ? 'text-green-600' : 'text-blue-600'
                                                    }`}>
                                                        {reward.required_points} pt
                                                    </span>
                                                    {canRedeem && !isOutOfStock && (
                                                        <button 
                                                            className="ml-2 px-3 py-1 bg-blue-500 text-white text-xs rounded-full hover:bg-blue-600 transition-colors"
                                                            onClick={() => handleRewardRedeem(reward.id)}
                                                        >
                                                            交換
                                                        </button>
                                                    )}
                                                </div>
                                            </li>
                                        );
                                    })
                                ) : (
                                    <li className="text-center text-gray-500 py-8">
                                        <Gift className="w-16 h-16 text-gray-300 mx-auto mb-2"/>
                                        <p>現在利用可能な特典がありません</p>
                                    </li>
                                )}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
