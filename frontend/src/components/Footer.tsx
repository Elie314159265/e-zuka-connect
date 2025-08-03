import Link from 'next/link';

export default function Footer() {
    const FooterLink = ({ href, children }: { href: string, children: React.ReactNode }) => (
        <Link href={href} className="text-gray-400 hover:text-white transition-colors">
            {children}
        </Link>
    );

    return (
        <footer className="bg-gray-800 text-white">
            <div className="container mx-auto px-6 py-8 text-center">
                <p className="font-bold text-lg mb-2">e-ZUKA CONNECT</p>
                <div className="flex justify-center space-x-6 mb-4">
                    <FooterLink href="/privacy">プライバシーポリシー</FooterLink>
                    <FooterLink href="/terms">利用規約</FooterLink>
                    <FooterLink href="/contact">お問い合わせ</FooterLink>
                </div>
                <p className="text-gray-500">&copy; 2025 e-ZUKA CONNECT. All Rights Reserved.</p>
            </div>
        </footer>
    );
}
