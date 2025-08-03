"use client";
import { motion } from 'framer-motion';
import Link from 'next/link';
import { MessageSquarePlus, Link as LinkIcon } from 'lucide-react';

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

export default function LineIntegrationPage() {
    return (
        <motion.div
            className="min-h-screen flex items-center justify-center bg-gray-50 py-24 px-4"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="max-w-2xl w-full text-center bg-white p-8 md:p-16 rounded-2xl shadow-lg">
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1, rotate: 10 }} transition={{ type: 'spring', delay: 0.2 }}>
                    <MessageSquarePlus className="w-24 h-24 text-green-500 mx-auto mb-6"/>
                </motion.div>
                <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">いつものLINEで、もっと便利に</h1>
                <p className="text-gray-600 max-w-md mx-auto mb-8">「e-ZUKA CONNECT」とLINEを連携すると、写真一枚でセール情報を発信したり、お客様へクーポンを届けたり。お店のファン作りが、もっと簡単になります。</p>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="w-full max-w-xs mx-auto bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors flex items-center justify-center space-x-2" type="button">
                    <LinkIcon className="w-6 h-6"/><span>LINEと連携する</span>
                </motion.button>
                <Link href="/" className="block text-sm text-gray-500 hover:text-gray-700 mt-8">トップページに戻る</Link>
            </div>
        </motion.div>
    );
}
