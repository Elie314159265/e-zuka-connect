"use client";
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { 
    Receipt, TicketPercent, BookOpen, Camera, DatabaseZap, Compass, 
    LayoutDashboard, MessageSquare, Sparkles, X, Award, Cake, Star, Lock, 
    Menu, Sun, CloudRain, BarChart3, PieChart, MessageSquarePlus, Link as LinkIcon,
    User, Mail, KeyRound
} from 'lucide-react';
import Link from 'next/link';


// NOTE: This is a temporary extraction.
// These components will be moved to their own files in /components later.

const pageVariants = {
    initial: { opacity: 0, scale: 0.99 },
    in: { opacity: 1, scale: 1 },
    out: { opacity: 0, scale: 0.99 }
};

const pageTransition = {
    type: 'tween',
    ease: 'anticipate',
    duration: 0.5
} as const;

const FadeInWhenVisible = ({ children, delay = 0, className = '' }: { children: React.ReactNode, delay?: number, className?: string }) => {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.2 });

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 20 }}
            transition={{ duration: 0.8, ease: 'easeOut', delay }}
            className={className}
        >
            {children}
        </motion.div>
    );
};

const ParticleCanvas = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    const drawParticles = useCallback(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let particlesArray: Particle[] = [];

        class Particle {
            x: number;
            y: number;
            size: number;
            speedX: number;
            speedY: number;
            color: string;

            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 1.5 + 1;
                this.speedX = Math.random() * 2 - 1;
                this.speedY = Math.random() * 2 - 1;
                this.color = 'rgba(255, 255, 255, 0.7)';
            }
            update() {
                if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
                if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
                this.x += this.speedX;
                this.y += this.speedY;
            }
            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        function init() {
            particlesArray = [];
            let numberOfParticles = (canvas.height * canvas.width) / 9000;
            for (let i = 0; i < numberOfParticles; i++) {
                particlesArray.push(new Particle());
            }
        }

        function connect() {
            let opacityValue = 1;
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) +
                                   ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                    if (distance < (canvas.width / 7) * (canvas.height / 7)) {
                        opacityValue = 1 - (distance / 20000);
                        ctx.strokeStyle = `rgba(255, 255, 255, ${opacityValue})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        let animationFrameId;
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particlesArray.forEach(p => {
                p.update();
                p.draw();
            });
            connect();
            animationFrameId = requestAnimationFrame(animate);
        }

        init();
        animate();

        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, []);

    useEffect(() => {
        const cleanup = drawParticles();
        window.addEventListener('resize', drawParticles);
        return () => {
            if(cleanup) cleanup();
            window.removeEventListener('resize', drawParticles);
        };
    }, [drawParticles]);

    return <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full" />;
};

const FeatureCard = ({ icon, title, text, delay = 0 }: { icon: React.ReactNode, title: string, text: string, delay?: number }) => (
    <FadeInWhenVisible delay={delay}>
        <motion.div 
            className="bg-gray-50 p-8 rounded-xl shadow-md h-full"
            whileHover={{ y: -5, boxShadow: "0 10px 20px rgba(0,0,0,0.1)" }}
            transition={{ duration: 0.3 }}
        >
            {icon}
            <h3 className="text-2xl font-bold mb-3">{title}</h3>
            <p className="text-gray-600">{text}</p>
        </motion.div>
    </FadeInWhenVisible>
);

const HowToStep = ({ icon, title, text, delay = 0 }: { icon: React.ReactNode, title: string, text: React.ReactNode, delay?: number }) => (
    <FadeInWhenVisible delay={delay} className="relative z-10">
        <div className="bg-white p-6 rounded-full w-24 h-24 mx-auto flex items-center justify-center shadow-lg mb-4">
            {icon}
        </div>
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="text-gray-600 mt-1">{text}</p>
    </FadeInWhenVisible>
);


export default function HomePage() {
    return (
        <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition}>
            {/* Hero Section */}
            <section className="relative h-screen flex items-center justify-center text-white">
                <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: "url('https://source.unsplash.com/1920x1080/?japan,street,warm')" }}></div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-black/10"></div>
                <ParticleCanvas />
                <div className="relative z-10 text-center px-6">
                    <motion.h1 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="text-4xl md:text-6xl font-bold mb-4 leading-tight tracking-tight" style={{ textShadow: "2px 2px 8px rgba(0,0,0,0.7)" }}>
                        一枚のレシートが、<br className="md:hidden" />まちの未来を変える。
                    </motion.h1>
                    <motion.p 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                        className="text-lg md:text-xl max-w-2xl mx-auto" style={{ textShadow: "1px 1px 4px rgba(0,0,0,0.7)" }}>
                        データと人の繋がりで、飯塚の商店街を元気に。新しい地域活性化プラットフォーム「e-ZUKA CONNECT」
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.6 }}
                    >
                        <Link href="/login/user"
                           className="mt-8 inline-block bg-white text-blue-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-all hover:scale-105 transform shadow-lg">
                            今すぐ始める
                        </Link>
                    </motion.div>
                </div>
            </section>
            
            {/* Features Section */}
            <section id="features" className="py-20 bg-white">
                <div className="container mx-auto px-6">
                    <FadeInWhenVisible className="text-center mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold">e-ZUKA CONNECTでできること</h2>
                        <p className="text-gray-600 mt-2">あなたの「いつも」が、まちの「特別」に変わる体験。</p>
                    </FadeInWhenVisible>
                    <div className="grid md:grid-cols-3 gap-8">
                        <FeatureCard 
                            icon={<div className="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center mb-6"><Receipt className="w-8 h-8" /></div>}
                            title="レシートで応援"
                            text="お買い物したレシートを撮るだけ。あなたの消費がデータとなり、お店の力になります。地域への貢献が、目に見える形で実感できます。"
                        />
                        <FeatureCard 
                            delay={0.2}
                            icon={<div className="bg-green-100 text-green-600 w-16 h-16 rounded-full flex items-center justify-center mb-6"><TicketPercent className="w-8 h-8" /></div>}
                            title="お得な発見"
                            text="地元のお店だけの限定クーポンや、楽しいイベント情報が満載。知らなかったお店を訪れる、新しいきっかけがここにあります。"
                        />
                        <FeatureCard 
                            delay={0.4}
                            icon={<div className="bg-yellow-100 text-yellow-600 w-16 h-16 rounded-full flex items-center justify-center mb-6"><BookOpen className="w-8 h-8" /></div>}
                            title="物語に触れる"
                            text="お店の歴史や店主のこだわり。商店街の魅力に触れるデジタルアーカイブ機能。街歩きがもっと楽しくなるストーリーに出会えます。"
                        />
                    </div>
                </div>
            </section>

            {/* How-to Section */}
            <section id="how-to" className="py-20 bg-gray-50">
                <div className="container mx-auto px-6 text-center">
                    <FadeInWhenVisible className="mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold">かんたん3ステップ</h2>
                        <p className="text-gray-600 mt-2">今日からあなたも、まちのサポーター。</p>
                    </FadeInWhenVisible>
                    <div className="relative grid md:grid-cols-3 gap-8 items-start">
                         <div className="hidden md:block absolute top-12 left-0 w-full h-px">
                            <svg width="100%" height="2"><line x1="0" y1="1" x2="100%" y2="1" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="8 8"/></svg>
                        </div>
                        <HowToStep icon={<Camera className="w-12 h-12 text-blue-600" />} title="1. 撮影する" text={<>お買い物をしたら<br/>レシートをパシャリ！</>} />
                        <HowToStep delay={0.2} icon={<DatabaseZap className="w-12 h-12 text-green-600" />} title="2. 貢献する" text={<>データがお店に届き<br/>ポイントも貯まる！</>} />
                        <HowToStep delay={0.4} icon={<Compass className="w-12 h-12 text-yellow-600" />} title="3. 発見する" text={<>新しいお店や<br/>まちの魅力を再発見！</>} />
                    </div>
                </div>
            </section>
            
            {/* For Owners Section */}
            <section className="py-20 bg-white">
                <div className="container mx-auto px-6 text-center">
                    <FadeInWhenVisible className="mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold">店舗オーナーの皆様へ</h2>
                        <p className="text-gray-600 mt-2">データとテクノロジーで、お店の経営を力強くサポートします。</p>
                    </FadeInWhenVisible>
                    <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                        <FadeInWhenVisible>
                             <motion.a href="/dashboard" className="group block bg-gray-50 p-8 rounded-xl shadow-md h-full" whileHover={{ y: -5, boxShadow: "0 10px 20px rgba(0,0,0,0.1)" }}>
                                <div className="bg-purple-100 text-purple-600 w-16 h-16 rounded-full flex items-center justify-center mb-6 mx-auto group-hover:scale-110 transition-transform"><LayoutDashboard className="w-8 h-8" /></div>
                                <h3 className="text-2xl font-bold mb-3">経営ダッシュボード</h3>
                                <p className="text-gray-600">売上や客層をリアルタイムに可視化。データに基づいた経営判断が可能になります。</p>
                             </motion.a>
                        </FadeInWhenVisible>
                        <FadeInWhenVisible delay={0.2}>
                             <motion.a href="/line-integration" className="group block bg-gray-50 p-8 rounded-xl shadow-md h-full" whileHover={{ y: -5, boxShadow: "0 10px 20px rgba(0,0,0,0.1)" }}>
                                <div className="bg-green-100 text-green-600 w-16 h-16 rounded-full flex items-center justify-center mb-6 mx-auto group-hover:scale-110 transition-transform"><MessageSquare className="w-8 h-8" /></div>
                                <h3 className="text-2xl font-bold mb-3">かんたんLINE連携</h3>
                                <p className="text-gray-600">いつものLINEで、セール情報やクーポンを手軽に発信。お客様との繋がりを深めます。</p>
                             </motion.a>
                        </FadeInWhenVisible>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="bg-blue-600 text-white">
                <div className="container mx-auto px-6 py-20 text-center">
                    <FadeInWhenVisible>
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">さあ、あなたも飯塚の未来に参加しませんか？</h2>
                    </FadeInWhenVisible>
                    <FadeInWhenVisible delay={0.2}>
                        <p className="text-lg max-w-2xl mx-auto mb-8">「e-ZUKA CONNECT」は、飯塚を愛するすべての人のためのプラットフォームです。<br/>あなたの参加が、このまちの新しい物語を創ります。</p>
                    </FadeInWhenVisible>
                    <FadeInWhenVisible delay={0.4}>
                        <Link href="/login/user" className="inline-block bg-white text-blue-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-all hover:scale-105 transform shadow-lg">
                            ログイン / 新規登録
                        </Link>
                    </FadeInWhenVisible>
                </div>
            </section>
        </motion.div>
    );
}
