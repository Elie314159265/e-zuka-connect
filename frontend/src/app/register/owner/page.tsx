"use client";
import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
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

const AuthPageLayout = ({ children }: { children: React.ReactNode }) => (
    <motion.div
        className="min-h-screen flex items-center justify-center bg-gray-50 py-24 px-4"
        initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
    >
        <div className="max-w-md w-full bg-white p-8 md:p-12 rounded-2xl shadow-lg">
            {children}
        </div>
    </motion.div>
);

export default function OwnerRegisterPage() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";

        let apiUrl = `${apiBaseUrl}/api/stores/owners/register`;
        if (apiUrl.startsWith('http:')) {
            apiUrl = apiUrl.replace('http:', 'https:');
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    email, 
                    password, 
                    full_name: name,
                    store_name: name // 店舗名として使用
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                let errorMessage = 'ユーザー登録に失敗しました。';
                
                if (errorData.detail) {
                    if (typeof errorData.detail === 'string') {
                        errorMessage = errorData.detail;
                    } else if (errorData.detail.message) {
                        // パスワード強度エラーなどの場合
                        errorMessage = errorData.detail.message;
                        if (errorData.detail.errors && errorData.detail.errors.length > 0) {
                            errorMessage += '\n' + errorData.detail.errors.join('\n');
                        }
                    }
                }
                
                throw new Error(errorMessage);
            }

            // 登録成功後、ログインページにリダイレクト
            router.push('/login/owner');

        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました。');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthPageLayout>
            <div className="text-center mb-8">
                <Link href="/" className="text-3xl font-bold text-gray-800 mb-2">e-ZUKA CONNECT</Link>
                <p className="text-gray-600">事業者様 新規アカウント作成</p>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">店舗・事業者名</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="〇〇商店" required />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">メールアドレス</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="email@example.com" required />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2">パスワード</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="******************" required />
                </div>
                {error && (
                    <div className="text-red-500 text-xs italic mb-4 text-center whitespace-pre-line">
                        {error}
                    </div>
                )}
                <div className="flex items-center justify-between">
                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }} 
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors disabled:opacity-50" 
                        type="submit"
                        disabled={isLoading}
                    >
                        {isLoading ? '登録中...' : 'アカウント作成'}
                    </motion.button>
                </div>
            </form>
            <p className="text-center text-gray-600 text-sm mt-8">
                すでにアカウントをお持ちですか？ <Link href="/login/owner" className="font-bold text-blue-600 hover:text-blue-800">ログイン</Link>
            </p>
        </AuthPageLayout>
    );
};
