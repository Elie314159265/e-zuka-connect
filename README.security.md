# セキュリティとシークレット管理

このドキュメントでは、プロジェクトの機密情報の管理方法について説明します。

## 機密情報を含むファイル

以下のファイルには機密情報が含まれており、Gitリポジトリには含まれていません：

### 1. データベース設定
- `services/core-api/alembic.ini` - データベース接続情報（パスワード含む）

**セットアップ方法**:
```bash
cp services/core-api/alembic.ini.example services/core-api/alembic.ini
# ファイルを編集してデータベース接続情報を設定
```

### 2. GCP サービスアカウント認証情報
- `services/ocr-processor/gcp-credentials.json` - GCP Document AI用の認証情報

**セットアップ方法**:
1. GCPコンソールでサービスアカウントキーを作成
2. ダウンロードしたJSONファイルを `services/ocr-processor/gcp-credentials.json` として保存

### 3. Kubernetesシークレット
- `kubernetes/base/cloudsql-secret.yaml` - Cloud SQLデータベースの認証情報
- `kubernetes/base/gcp-ocr-credentials-secret.yaml` - GCP認証情報のKubernetesシークレット

**セットアップ方法**:
```bash
# データベースシークレット
cp kubernetes/base/cloudsql-secret.yaml.example kubernetes/base/cloudsql-secret.yaml
# ファイルを編集してusernameとpasswordを設定

# GCP認証情報シークレット
cp kubernetes/base/gcp-ocr-credentials-secret.yaml.example kubernetes/base/gcp-ocr-credentials-secret.yaml
# ファイルを編集してGCP認証情報を設定
```

### 4. フロントエンド環境変数
- `frontend/.env.local` - ローカル開発環境用の環境変数

**セットアップ方法**:
```bash
cp frontend/.env.local.example frontend/.env.local
# 必要に応じてAPIのURLを変更
```

## .gitignoreに含まれるパターン

以下のファイル/ディレクトリは自動的にGitから除外されます：

- `*-secret.yaml` - すべてのKubernetesシークレットファイル
- `**/gcp-credentials.json` - GCP認証情報
- `**/*-credentials.json` - すべての認証情報ファイル
- `*.pem`, `*.key` - 秘密鍵ファイル
- `alembic.ini` - データベース設定ファイル
- `.env.local`, `.env.*.local` - ローカル環境変数
- `*-changes.txt` - 変更履歴ファイル（個人情報を含む可能性）

## 本番環境へのデプロイ

本番環境では、機密情報をKubernetesシークレットとして管理します：

```bash
# シークレットの作成
kubectl apply -f kubernetes/base/cloudsql-secret.yaml -n your-gcp-project-id
kubectl apply -f kubernetes/base/gcp-ocr-credentials-secret.yaml -n your-gcp-project-id

# シークレットの確認
kubectl get secrets -n your-gcp-project-id

# シークレットの内容確認（base64デコード）
kubectl get secret cloudsql-secret -n your-gcp-project-id -o jsonpath='{.data.username}' | base64 -d
```

## セキュリティのベストプラクティス

1. **機密情報は絶対にGitにコミットしない**
   - `.gitignore`が正しく設定されていることを確認
   - コミット前に `git status` で確認

2. **定期的にシークレットをローテーション**
   - データベースパスワードを定期的に変更
   - サービスアカウントキーを定期的に更新

3. **最小権限の原則**
   - サービスアカウントには必要最小限の権限のみ付与
   - データベースユーザーも必要な権限のみ

4. **環境変数の分離**
   - 開発、ステージング、本番で異なる認証情報を使用
   - `.env.local`は開発環境専用

5. **監査ログ**
   - GCPの監査ログで不正アクセスを監視
   - データベースアクセスログを確認

## トラブルシューティング

### Gitに機密情報をコミットしてしまった場合

```bash
# 特定のファイルを履歴から削除（BFG Repo-Cleanerを使用）
# https://rtyley.github.io/bfg-repo-cleaner/

# または git filter-branch を使用
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch PATH_TO_FILE" \
  --prune-empty --tag-name-filter cat -- --all

# リモートに強制プッシュ（注意！）
git push origin --force --all
```

**重要**: 機密情報が漏洩した場合は、直ちにシークレットを無効化・再生成してください。

## お問い合わせ

セキュリティに関する質問や問題が発生した場合は、プロジェクト管理者に連絡してください。
