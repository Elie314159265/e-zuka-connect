"use client";
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles } from 'lucide-react';

interface AiAdviceModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function AiAdviceModal({ isOpen, onClose }: AiAdviceModalProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [advice, setAdvice] = useState('');
    const [error, setError] = useState('');

    const fetchAdvice = async () => {
        setIsLoading(true);
        setAdvice('');
        setError('');

        const prompt = "あなたは福岡県飯塚市にある個人商店の、親しみやすく励ましてくれる経営コンサルタントです。以下のデータに基づき、売上を向上させるための具体的で分かりやすい行動案を3つ提案してください。日本語で、箇条書きや番号付きリストを使って回答をフ���ーマットしてください。データ: [売上傾向: 今月は微減。天気の影響: 雨の日に売上が落ちる。人気商品: 1. 特製からあげ弁当, 2. 日替わり定食, 3. チキン南蛮。主な客層: サラリーマンや地元住民。]";

        try {
            // IMPORTANT: API Key should be handled securely, e.g., via environment variables and a backend proxy.
            const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY;
            if (!apiKey) {
                // This is a mock response for when the API key is not set.
                console.warn("NEXT_PUBLIC_GEMINI_API_KEY is not set. Using mock data.");
                setAdvice("AIアドバイスのデモです:\n\n1. **雨の日限定セット割:** 雨の日は客足が遠のくようですので、「からあげ弁当 + 温かいお茶」のセットを50円引きで提供してみてはいかがでしょうか。\n\n2. **ランチタイムの看板:** お店の前を通るサラリーマン向けに、日替わり定食の内容を写真付きでアピールする看板を出すと効果的です。\n\n3. **ポイントカード導入:** 地元の常連さん向けに、500円で1ポイント貯まり、20ポイントでからあげ1個サービスのようなポイントカードを始めると、再来店に繋がりますよ！");
                setIsLoading(false);
                return;
            }

            const chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
            const payload = { contents: chatHistory };
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorBody = await response.text();
                console.error("API Error Response:", errorBody);
                throw new Error(`API request failed with status ${response.status}`);
            }

            const result = await response.json();

            if (result.candidates?.[0]?.content?.parts?.[0]?.text) {
                const text = result.candidates[0].content.parts[0].text;
                setAdvice(text);
            } else {
                console.error("Unexpected API response format:", result);
                throw new Error('AIからの応答が予期した形式ではありません。');
            }
        } catch (err) {
            console.error("Error calling Gemini API:", err);
            setError('AIからのアドバイスの取得に失敗しました。APIキーが正しく設定されているか確認してください。');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchAdvice();
        }
    }, [isOpen]);

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="fixed inset-0 bg-black/60 z-[110] flex items-center justify-center p-4 backdrop-blur-sm"
                >
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        onClick={(e) => e.stopPropagation()}
                        className="bg-white rounded-2xl shadow-lg max-w-2xl w-full p-8 relative"
                    >
                        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
                            <X className="w-6 h-6" />
                        </button>
                        <div className="text-center">
                            <Sparkles className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                            <h2 className="text-2xl font-bold mb-4">AI経営アドバイザーからの提案</h2>
                        </div>
                        <div className="mt-6 text-left max-h-[60vh] overflow-y-auto pr-4 text-gray-700 space-y-4">
                            {isLoading && (
                                <div className="flex flex-col items-center justify-center h-48">
                                    <motion.div
                                        animate={{ rotate: 360 }}
                                        transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                                        className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full"
                                    />
                                    <p className="mt-4 text-gray-500">AIが分析中です...</p>
                                </div>
                            )}
                            {error && <p className="text-red-500 text-center">{error}</p>}
                            {advice && <div className="prose max-w-none whitespace-pre-wrap">{advice}</div>}
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}