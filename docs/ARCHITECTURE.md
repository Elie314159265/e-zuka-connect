# E-Zuka Connect アーキテクチャ設計

## アーキテクチャ概要

E-Zuka Connectは、Google Kubernetes Engine (GKE) 上にマイクロサービスアーキテクチャを採用した、スケーラブルで高可用性なWebアプリケーションです。

## アーキテクチャ設計思想

### なぜマイクロサービスか

1. **スケーラビリティ**: 各サービスを独立してスケール可能
   - イベント時のレシートアップロード集中に対応
   - 特定サービスのみをスケールさせることで効率的なリソース利用

2. **開発速度**: サービスごとに並行開発が可能
   - チームを分離して開発を進められる
   - 各サービスに最適な技術スタックを選択可能

3. **保守性**: 疎結合な設計
   - 1つのサービスの変更が他に影響を与えにくい
   - デプロイの独立性

## システム構成

### マイクロサービス一覧

1. **Core API Service** (FastAPI)
   - ユーザー認証・認可 (JWT)
   - レシート管理
   - 店舗管理
   - データ分析API

2. **OCR Processor Service** (FastAPI)
   - Google Document AI連携
   - レシート画像からテキスト抽出
   - 構造化データの生成

3. **AI Advisor Service** (FastAPI)
   - Google Gemini API連携
   - 経営アドバイス生成
   - データ分析結果の解釈

4. **Frontend** (Next.js 14)
   - ユーザーインターフェース
   - App Router使用
   - サーバーサイドレンダリング

### インフラストラクチャ

#### Google Cloud Platform (GCP)

- **GKE (Google Kubernetes Engine)**
  - マイクロサービスのオーケストレーション
  - 自動スケーリング
  - ローリングアップデート

- **Cloud SQL for PostgreSQL**
  - マネージドデータベース
  - 高可用性構成
  - 自動バックアップ

- **Cloud Storage**
  - レシート画像の保存
  - 静的ファイルのホスティング

- **Document AI**
  - レシートOCR処理
  - 構造化データ抽出

#### Kubernetes リソース

- **Deployments**: 各マイクロサービスの管理
- **Services**: サービス間通信
- **Ingress**: 外部からのアクセス制御
- **ConfigMaps**: 環境変数管理
- **Secrets**: 機密情報管理（別途作成が必要）
- **CronJobs**: 定期処理
  - 天候データ取得
  - プロモーション配信

## データフロー

### レシートアップロードフロー

```
1. ユーザー (Frontend)
   ↓ レシート画像アップロード
2. Core API
   ↓ 画像をGCSに保存
   ↓ OCR処理リクエスト
3. OCR Processor
   ↓ Document AI呼び出し
   ↓ 構造化データ返却
4. Core API
   ↓ データベースに保存
   ↓ ポイント計算
5. ユーザーに結果返却
```

### AI経営アドバイスフロー

```
1. 店舗オーナー (Frontend)
   ↓ アドバイス生成リクエスト
2. Core API
   ↓ 売上データ・天候データ取得
   ↓ AI Advisorにリクエスト
3. AI Advisor Service
   ↓ Gemini API呼び出し
   ↓ プロンプト生成・解析
4. 経営アドバイス返却
```

## セキュリティ設計

### 認証・認可

- **JWT (JSON Web Tokens)**: ステートレス認証
- **Access Token**: 15分有効期限
- **Refresh Token**: 30日有効期限
- **bcrypt**: パスワードハッシュ化

### ネットワークセキュリティ

- **HTTPS**: すべての通信を暗号化
- **CORS**: 適切なオリジン制限
- **Ingress**: 外部からのアクセス制御

### データ保護

- **Cloud SQL**: プライベートIP接続
- **Secrets**: Kubernetes Secretsでの管理
- **環境変数**: ConfigMapsでの管理

## データベース設計

### 主要テーブル

- **users**: ユーザー情報
- **store_owners**: 店舗オーナー情報
- **stores**: 店舗情報
- **receipts**: レシート情報
- **receipt_items**: レシート明細
- **gamification_profiles**: ゲーミフィケーション情報
- **user_badges**: バッジ獲得履歴
- **point_transactions**: ポイント取引履歴
- **weather_data**: 天候データ
- **promotions**: プロモーション情報

## スケーリング戦略

### 水平スケーリング

- Kubernetes HPA (Horizontal Pod Autoscaler)
- CPU使用率ベースの自動スケーリング
- イベント時の一時的なスケールアップ

### 垂直スケーリング

- 必要に応じてPodのリソース制限を調整
- データベースインスタンスのスケールアップ

## モニタリング・ログ

### ログ戦略

- 構造化ログ (JSON形式)
- Cloud Logging連携
- セキュリティイベントの追跡

### メトリクス

- アプリケーションメトリクス
- インフラメトリクス
- ビジネスメトリクス（売上、ユーザー数等）

## デプロイメント戦略

### CI/CD

- GitHubリポジトリ
- Docker イメージビルド
- GKEへのデプロイ

### デプロイメント手順

```bash
# イメージビルド
docker build -t asia-northeast1-docker.pkg.dev/PROJECT_ID/REPO/SERVICE:TAG .

# イメージプッシュ
docker push asia-northeast1-docker.pkg.dev/PROJECT_ID/REPO/SERVICE:TAG

# Kubernetesデプロイ
kubectl apply -k kubernetes/base/
```

## 今後の拡張計画

### フェーズ2: 機能拡張

- LINE連携
- プッシュ通知
- リアルタイム分析

### フェーズ3: スケーリング

- マルチリージョン対応
- CDN統合
- キャッシュ戦略の最適化

## 参考資料

- [プロジェクト概要](./PROJECT_OVERVIEW.md)
- [開発ログ](./DEVELOPMENT_LOG.md)
