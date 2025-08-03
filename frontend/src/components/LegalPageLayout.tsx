"use client";
import { motion } from 'framer-motion';
import Link from 'next/link';

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

export default function LegalPageLayout({ title, children }: { title: string, children: React.ReactNode }) {
    return (
        <motion.div
            className="min-h-screen bg-white py-24"
            initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}
        >
            <div className="container mx-auto px-6 max-w-4xl">
                <h1 className="text-4xl font-bold mb-8">{title}</h1>
                <div className="prose max-w-none text-gray-700">
                    {children}
                </div>
                <div className="text-center mt-12">
                    <Link href="/" className="bg-blue-600 text-white px-6 py-3 rounded-full font-bold hover:bg-blue-700 transition-transform hover:scale-105">
                        トップページに戻る
                    </Link>
                </div>
            </div>
        </motion.div>
    );
}
