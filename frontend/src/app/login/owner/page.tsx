"use client";
import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '../../../store/authStore';

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

export default function OwnerLoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const { setToken } = useAuthStore();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://your-gcp-project-id.com";
        
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);

        let apiUrl = `${apiBaseUrl}/api/stores/owners/login`;
        if (apiUrl.startsWith('http:')) {
            apiUrl = apiUrl.replace('http:', 'https:');
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: params,
            });

            if (!response.ok) {
                let errorMessage = 'ログインに失敗しました。';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (jsonError) {
                    // JSONパースエラーの場合はHTMLレスポンスの可能性があるため
                    const textResponse = await response.text();
                    if (textResponse.includes('Internal Server Error')) {
                        errorMessage = 'サーバーエラーが発生しました。しばらく時間をおいて再度お試しください。';
                    }
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            
            setToken(data.access_token);

            // Redirect to dashboard
            router.push('/dashboard');

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
                <p className="text-gray-600">事業者様ログイン</p>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label htmlFor="login-email" className="block text-gray-700 text-sm font-bold mb-2">メールアドレス</label>
                    <input type="email" id="login-email" value={email} onChange={(e) => setEmail(e.target.value)} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="email@example.com" required />
                </div>
                <div className="mb-6">
                    <label htmlFor="login-password" className="block text-gray-700 text-sm font-bold mb-2">パスワード</label>
                    <input type="password" id="login-password" value={password} onChange={(e) => setPassword(e.target.value)} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 mb-3 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="******************" required />
                    <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">パスワードを忘れましたか？</Link>
                </div>
                {error && <p className="text-red-500 text-xs italic mb-4 text-center">{error}</p>}
                <div className="flex items-center justify-between">
                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }} 
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors disabled:opacity-50" 
                        type="submit"
                        disabled={isLoading}
                    >
                        {isLoading ? 'ログイン中...' : 'ログイン'}
                    </motion.button>
                </div>
            </form>
            <p className="text-center text-gray-600 text-sm mt-8">
                アカウントをお持ちでないですか？ <Link href="/register/owner" className="font-bold text-blue-600 hover:text-blue-800">新規登録</Link>
            </p>
        </AuthPageLayout>
    );
};

