"use client";
import { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, ChevronDown } from 'lucide-react';

const DropdownMenu = ({ title, children }: { title: string, children: React.ReactNode }) => {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <div className="relative" onMouseEnter={() => setIsOpen(true)} onMouseLeave={() => setIsOpen(false)}>
            <button className="flex items-center text-gray-600 hover:text-blue-600 transition-colors py-2 md:py-0">
                {title}
                <ChevronDown className="w-4 h-4 ml-1" />
            </button>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute top-full mt-2 w-40 bg-white rounded-lg shadow-xl py-2"
                    >
                        {children}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

const DropdownLink = ({ href, children, onClick }: { href: string, children: React.ReactNode, onClick: () => void }) => (
    <Link href={href} onClick={onClick} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
        {children}
    </Link>
);

export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const isLoggedIn = false; // TODO: Replace with actual auth state

    const closeAllMenus = () => {
        setIsMenuOpen(false);
    };

    const navLinksLoggedOut = (
        <>
            <Link href="/#features" onClick={closeAllMenus} className="text-gray-600 hover:text-blue-600 transition-colors py-2 md:py-0">機能紹介</Link>
            <Link href="/#how-to" onClick={closeAllMenus} className="text-gray-600 hover:text-blue-600 transition-colors py-2 md:py-0">使い方</Link>
            
            {/* Desktop Dropdowns */}
            <div className="hidden md:flex items-center space-x-4">
                <DropdownMenu title="ログイン">
                    <DropdownLink href="/login/user" onClick={closeAllMenus}>お客様</DropdownLink>
                    <DropdownLink href="/login/owner" onClick={closeAllMenus}>事業者様</DropdownLink>
                </DropdownMenu>
                <DropdownMenu title="新規登録">
                    <DropdownLink href="/register/user" onClick={closeAllMenus}>お客様</DropdownLink>
                    <DropdownLink href="/register/owner" onClick={closeAllMenus}>事業者様</DropdownLink>
                </DropdownMenu>
            </div>

            {/* Mobile Links */}
            <div className="md:hidden flex flex-col items-center space-y-4 mt-4">
                <p className="font-bold text-gray-700">ログイン</p>
                <Link href="/login/user" onClick={closeAllMenus} className="text-blue-600">お客様はこちら</Link>
                <Link href="/login/owner" onClick={closeAllMenus} className="text-blue-600">事業者様はこちら</Link>
                <p className="font-bold text-gray-700 mt-4">新規登録</p>
                <Link href="/register/user" onClick={closeAllMenus} className="text-blue-600">お客様はこちら</Link>
                <Link href="/register/owner" onClick={closeAllMenus} className="text-blue-600">事業者様はこちら</Link>
            </div>
        </>
    );

    const navLinksLoggedIn = (
        <>
            <Link href="/dashboard" onClick={closeAllMenus} className="text-gray-600 hover:text-blue-600 transition-colors py-2 md:py-0">ダッシュボード</Link>
            <Link href="/mypage" onClick={closeAllMenus} className="text-gray-600 hover:text-blue-600 transition-colors py-2 md:py-0">マイページ</Link>
            <button onClick={() => { /* TODO: handle logout */ closeAllMenus(); }}
               className="bg-gray-600 text-white px-4 py-2 rounded-full font-bold hover:bg-gray-700 transition-transform hover:scale-105">
                ログアウト
            </button>
        </>
    );

    return (
        <header className="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50 shadow-sm">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                <Link href="/" className="text-2xl font-bold text-gray-800">
                    e-ZUKA CONNECT
                </Link>
                <nav className="hidden md:flex items-center space-x-8">
                    {isLoggedIn ? navLinksLoggedIn : navLinksLoggedOut}
                </nav>
                <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                    <Menu className="w-6 h-6" />
                </button>
            </div>
            <AnimatePresence>
                {isMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden bg-white/90 backdrop-blur-md"
                    >
                        <nav className="flex flex-col items-center space-y-4 py-4">
                            {isLoggedIn ? navLinksLoggedIn : navLinksLoggedOut}
                        </nav>
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
}
