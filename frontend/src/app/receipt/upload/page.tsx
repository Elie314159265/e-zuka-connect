"use client";
import { useState } from 'react';
import { motion } from 'framer-motion';
import { UploadCloud, Loader, Send, CheckCircle, AlertTriangle } from 'lucide-react';

export default function ReceiptUploadPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [ocrResult, setOcrResult] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result as string);
            };
            reader.readAsDataURL(file);
            setOcrResult(null);
            setError(null);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedFile) {
            setError("まずファイルを選択してください。");
            return;
        }

        setIsLoading(true);
        setError(null);
        setOcrResult(null);

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch("/api/receipts/upload", {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || '解析に失敗しました。');
            }
            
            setOcrResult(data.ocr_result);

        } catch (err) {
            setError(err instanceof Error ? err.message : '不明なエラーが発生しました。');
        } finally {
            setIsLoading(false);
        }
    };
    
    // TODO: Implement the confirmation logic
    const handleConfirm = () => {
        alert("（TODO: この内容でデータベースに保存する処理を実装します）");
    };

    return (
        <div className="min-h-screen bg-gray-50 py-24 px-4">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-8">レシートアップロード</h1>
                
                <form onSubmit={handleSubmit} className="bg-white p-8 rounded-2xl shadow-lg">
                    <div className="mb-6">
                        <label htmlFor="receipt-upload" className="cursor-pointer block border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50 transition-colors">
                            <UploadCloud className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                            <span className="text-lg font-semibold text-gray-600">クリックしてファイルを選択</span>
                            <p className="text-gray-500 text-sm mt-1">（または、ここにドラッグ＆ドロップ）</p>
                        </label>
                        <input id="receipt-upload" type="file" className="hidden" onChange={handleFileChange} accept="image/png, image/jpeg" />
                    </div>

                    {preview && (
                        <div className="mb-6 text-center">
                            <h3 className="text-lg font-semibold mb-2">プレビュー</h3>
                            <img src={preview} alt="Receipt preview" className="max-w-full max-h-64 mx-auto rounded-lg shadow-md" />
                        </div>
                    )}

                    <motion.button 
                        type="submit"
                        disabled={!selectedFile || isLoading}
                        className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center space-x-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                        whileHover={{ scale: !(!selectedFile || isLoading) ? 1.05 : 1 }}
                        whileTap={{ scale: !(!selectedFile || isLoading) ? 0.95 : 1 }}
                    >
                        {isLoading ? <Loader className="animate-spin" /> : <Send />}
                        <span>{isLoading ? '解析中...' : 'レシートを解析する'}</span>
                    </motion.button>
                </form>

                {error && (
                    <div className="mt-6 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg flex items-center">
                        <AlertTriangle className="w-6 h-6 mr-3" />
                        <div>
                            <p className="font-bold">エラー</p>
                            <p>{error}</p>
                        </div>
                    </div>
                )}

                {ocrResult && (
                    <div className="mt-6 bg-white p-8 rounded-2xl shadow-lg">
                        <h2 className="text-2xl font-bold mb-4 flex items-center"><CheckCircle className="w-8 h-8 text-green-500 mr-3" /> 解析結果</h2>
                        <div className="space-y-2 text-gray-700">
                            <p><strong>店名:</strong> {ocrResult.supplier_name || 'N/A'}</p>
                            <p><strong>合計金額:</strong> {ocrResult.total_amount || 'N/A'}</p>
                            <h3 className="text-lg font-semibold pt-2">購入品目:</h3>
                            <ul className="list-disc list-inside pl-4">
                                {ocrResult.line_items.map((item, index) => (
                                    <li key={index}>{item.description} - {item.amount}</li>
                                ))}
                            </ul>
                        </div>
                        <button 
                            onClick={handleConfirm}
                            className="mt-6 w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 transition-colors"
                        >
                            この内容で登録する
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
