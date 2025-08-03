# ステージ1: 依存関係のインストールとアプリケーションのビルド
FROM node:18-alpine AS builder

# ビルド時の引数としてAPIのベースURLを��義
ARG NEXT_PUBLIC_API_BASE_URL=https://your-gcp-project-id.com

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY . .

# アプリケーションをビルド
RUN NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL npm run build

# ステージ2: 本番環境用の軽量イメージを作成
FROM node:18-alpine

WORKDIR /app

# ビルドステージから必要なファイルのみをコピー
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# ポートを開放
EXPOSE 3000

# アプリケーションを起動
CMD ["npm", "start"]
