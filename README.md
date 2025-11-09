# e-ZUKA Connect

データ駆動型イベント・店舗支援プラットフォーム - 福岡県飯塚市の商店街活性化プロジェクト

## 概要について

e-ZUKA Connectは、福岡県飯塚市の商店街活性化を目指すWebアプリケーションです。レシートOCRによるデータ収集、気象データとの相関分析、AI経営アドバイスなど、データに基づいた販促支援を提供します。

### 主要機能

- **レシートOCR機能**: Google Document AIを使用した高精度レシート読み取り
- **データ分析機能**: 天候データと売上データの相関分析、顧客層分析
- **ゲーミフィケーション**: ポイント・バッジ・レベルシステムでユーザーエンゲージメント向上
- **AI経営アドバイス**: Gemini APIを活用したデータに基づく経営アドバイス
- **プロモーション管理**: クーポン・イベント管理機能

## 技術スタック

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion
- Zustand

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy
- Google Cloud Platform
  - Document AI (OCR)
  - Cloud Storage (画像保存)
  - Cloud SQL (データベース)
- Open-Meteo API (気象データ)
- Google Gemini API (AI経営アドバイス)

### Infrastructure
- Kubernetes (GKE)
- Docker
- Nginx Ingress Controller

## セットアップ

### 必要な環境

- Node.js 18以上
- Python 3.11以上
- Docker
- Google Cloud Platform アカウント
- PostgreSQL 13以上

### 環境変数の設定

各サービスで以下の環境変数が必要です。詳細な設定方法はドキュメントを参照してください。

#### Core API (.env または環境変数)

```bash
# データベース設定
DB_USER=your-database-username
DB_PASSWORD=your-database-password
DB_HOST=localhost  # ローカル開発時はlocalhost、Cloud SQLの場合は適宜変更
DB_PORT=5432
DB_NAME=your-database-name

# JWT認証設定
JWT_SECRET_KEY=your-jwt-secret-key-here  # 安全な鍵を生成してください
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-here  # リフレッシュトークン用

# GCP設定
GCP_PROJECT_ID=your-gcp-project-id
```

#### OCR Processor (.env または環境変数)

```bash
# GCP Document AI設定
GCP_PROJECT_ID=your-gcp-project-id
DOCAI_LOCATION=us  # またはアジアリージョン等
DOCAI_PROCESSOR_ID=your-document-ai-processor-id

# GCP認証情報（サービスアカウントキーのパス）
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

#### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # 開発環境
# NEXT_PUBLIC_API_BASE_URL=https://your-domain.com  # 本番環境
```

### JWT秘密鍵の生成

```bash
# Python3を使って安全な鍵を生成
python3 -c "import secrets, base64; print('JWT_SECRET_KEY=' + base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
python3 -c "import secrets, base64; print('JWT_REFRESH_SECRET_KEY=' + base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
```

### ローカル開発環境のセットアップ

#### 1. リポジトリのクローン

```bash
git clone https://github.com/Elie314159265/e-zuka-connect.git
cd e-zuka-connect
```

#### 2. Frontend のセットアップ

```bash
cd frontend
npm install
npm run dev
```

Frontend は `http://localhost:3000` で起動します。

#### 3. Core API のセットアップ

```bash
cd services/core-api
pip install -r requirements.txt

# 環境変数設定後に起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Core API は `http://localhost:8000` で起動します。

#### 4. OCR Processor のセットアップ

```bash
cd services/ocr-processor
pip install -r requirements.txt

# GCP認証情報の設定
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# 起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

OCR Processor は `http://localhost:8001` で起動します。

### データベースのセットアップ

```bash
# PostgreSQLに接続してデータベース作成
psql -U postgres
CREATE DATABASE your_database_name;

# Alembicマイグレーションを実行（初期化）
cd services/core-api
alembic upgrade head
```

## 開発コマンド

### Frontend (Next.js)
```bash
cd frontend
npm run dev        # 開発サーバー起動 (localhost:3000)
npm run build      # 本番ビルド
npm run start      # 本番サーバー起動
npm run lint       # ESLint実行
```

### Backend Services
```bash
# Core API (FastAPI)
cd services/core-api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# OCR Processor (FastAPI)
cd services/ocr-processor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Kubernetesへのデプロイ

### 1. Kubernetes Secretsの作成

```bash
# JWT秘密鍵のSecret作成
kubectl create secret generic jwt-secrets \
  --from-literal=JWT_SECRET_KEY='your-jwt-secret-key' \
  --from-literal=JWT_REFRESH_SECRET_KEY='your-refresh-secret-key' \
  -n e-zuka-connect

# データベース認証情報のSecret作成
kubectl create secret generic cloudsql-secret \
  --from-literal=DB_USER='your-db-user' \
  --from-literal=DB_PASSWORD='your-db-password' \
  -n e-zuka-connect

# GCP認証情報のSecret作成
kubectl create secret generic gcp-ocr-credentials-secret \
  --from-file=key.json=/path/to/service-account-key.json \
  -n e-zuka-connect
```

### 2. ConfigMapの設定

`kubernetes/base/configmap.yaml` を編集して環境に合わせた設定を行ってください。

### 3. デプロイ

```bash
# kubectl applyでリソースデプロイ
kubectl apply -f kubernetes/base/
```

## API ドキュメント

各サービスはFastAPIの自動生成ドキュメントを提供しています：

- Core API: `http://localhost:8000/docs`
- OCR Processor: `http://localhost:8001/docs`

## プロジェクト構造

```
e-zuka-connect/
├── frontend/                 # Next.js フロントエンド
│   ├── app/                 # App Router
│   ├── components/          # Reactコンポーネント
│   └── store/              # Zustand状態管理
├── services/
│   ├── core-api/           # メインAPIサービス
│   │   ├── app/
│   │   │   ├── routers/   # APIルート定義
│   │   │   ├── models/    # データベースモデル
│   │   │   └── security/  # 認証機能
│   │   └── requirements.txt
│   ├── ocr-processor/      # レシートOCR処理サービス
│   │   └── app/
│   └── ai-advisor/         # AI経営アドバイスサービス
│       └── app/
├── kubernetes/             # Kubernetes設定
│   ├── base/              # 基本設定
│   └── overlays/          # 環境別設定
├── docs/                  # プロジェクトドキュメント

```

## セキュリティと機密情報について

### 重要: 機密情報の取り扱い

このリポジトリは公開用リポジトリです。以下の機密情報はにコミット・プッシュしないでください：

**公開厳禁の機密ファイル例**:
- `.env`, `.env.local` などの環境変数ファイル
- GCP サービスアカウント鍵 (`.json`)
- データベースダンプ (`.sql`)
- Kubernetes Secrets (`.yaml`)←又は暗号化してください

### ローカル設定ファイルについて

このリポジトリはローカル開発用設定ファイルを含んでいません。上記のセットアップ手順に従って、各自で環境変数を設定してください。ローカル開発では機密情報を含む設定ファイルを使用しますが、これらは `.gitignore` によってGit管理から除外されています。

**本番環境では必ず環境変数経由で設定を行ってください。**

## このプロジェクトについて

- This project is for portfolio purposes.
- このプロジェクトはe-ZUKAスマートアプリコンテスト2025で企業賞を3社から受賞


## 開発者・貢献者

- **GitHub**: [Elie](https://github.com/Elie314159265)
- **Portfolio**: [Elie's Portfolio Site](https://portfolio-eight-phi-97.vercel.app/)

## サポート・お問い合わせ

質問や問題がある場合はGitHubのIssuesをご利用ください。
