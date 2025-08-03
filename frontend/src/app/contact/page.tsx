"use client";
import { motion } from 'framer-motion';

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

export default function ContactPage() {
    return (
        <motion.div
            className="min-h-screen flex items-center justify-center bg-gray-50 py-24 px-4"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="max-w-xl w-full bg-white p-8 md:p-12 rounded-2xl shadow-lg">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-800 mb-2">お問い合わせ</h1>
                    <p className="text-gray-600">ご意見・ご質問など、お気軽にお問い合わせください。</p>
                </div>
                <form>
                    <div className="mb-4"><label className="block text-gray-700 text-sm font-bold mb-2">お名前</label><input type="text" className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="山田 太郎"/></div>
                    <div className="mb-4"><label className="block text-gray-700 text-sm font-bold mb-2">メールアドレス</label><input type="email" className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="email@example.com"/></div>
                    <div className="mb-6"><label className="block text-gray-700 text-sm font-bold mb-2">お問い合わせ内容</label><textarea rows={5} className="shadow-sm appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="お問い合わせ内容をご入力ください..."></textarea></div>
                    <div className="flex items-center justify-between"><motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors" type="button">送信する</motion.button></div>
                </form>
            </div>
        </motion.div>
    );
}
