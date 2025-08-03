import type { Metadata } from "next";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: "e-ZUKA CONNECT",
  description: "データと人の繋がりで、飯塚の商店街を元気に。新しい地域活性化プラットフォーム「e-ZUKA CONNECT」",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className="bg-gray-50 text-gray-800 font-sans">
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

