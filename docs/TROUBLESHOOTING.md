# トラブルシューティングガイド

e-zuka-connectプラットフォームの開発・デプロイ時に発生した技術的課題と解決策をまとめたドキュメントです。

## 目次

1. [認証関連の問題](#認証関連の問題)
2. [データベース・Cloud SQL](#データベースcloud-sql)
3. [AIサービス](#aiサービス)
4. [Kubernetes・ネットワーク](#kubernetesネットワーク)
5. [フロントエンド・API連携](#フロントエンドapi連携)

---

## 認証関連の問題

### bcryptライブラリ互換性問題

**問題**: v1.3.5からv1.4.0+へのアップデート後、ユーザーログインが不可能

**エラーメッセージ**:
```
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**原因**:
- bcrypt 5.0.0でAPIに破壊的変更（`__about__`属性が削除）
- passlib 1.7.4がbcrypt 5.0.0に非対応
- バージョン固定なしで自動的にbcrypt 5.0.0へアップグレードされた

**解決策**:

1. `services/core-api/requirements.txt`でbcryptバージョンを固定:
   ```
   bcrypt==4.0.1
   passlib[bcrypt]
   ```

2. Dockerイメージを再ビルド:
   ```bash
   cd services/core-api
   docker build -t asia-northeast1-docker.pkg.dev/PROJECT_ID/REPO/core-api:TAG .
   docker push asia-northeast1-docker.pkg.dev/PROJECT_ID/REPO/core-api:TAG
   ```

3. Kubernetesデプロイメントを更新して再デプロイ

**検証方法**:
```bash
# Podログで正常起動を確認
kubectl logs -l app=core-api

# ログインエンドポイントをテスト
curl -X POST http://YOUR_DOMAIN/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}'
```

**関連ファイル**: `docs/development-logs/2025-09-29-bcrypt-error.txt`

---

## データベース・Cloud SQL

### Cloud SQL Proxy接続エラー

**問題**: GKE PodからCloud SQLに接続できない

**よくあるエラー**:
```
sqlalchemy.exc.OperationalError: could not connect to server
psycopg2.OperationalError: FATAL: password authentication failed
```

**解決策**:

#### 方法1: Cloud SQL Proxyサイドカーコンテナ
```yaml
# deployment.yamlに追加
containers:
- name: cloudsql-proxy
  image: gcr.io/cloudsql-docker/gce-proxy:latest
  command:
    - "/cloud_sql_proxy"
    - "-instances=PROJECT_ID:REGION:INSTANCE_NAME=tcp:5432"
```

#### 方法2: Workload Identity
1. GKEクラスタでWorkload Identityを有効化
2. Kubernetes Service Accountを作成
3. Cloud SQL ClientロールのあるGoogle Service Accountにバインド

#### 方法3: パブリックIPとSSL
- Cloud SQLインスタンスでパブリックIPを有効化
- SSL証明書を設定
- 承認済みネットワークを追加

**検証方法**:
```bash
# Pod内からデータベース接続をテスト
kubectl exec -it POD_NAME -- psql -h localhost -U USER -d DATABASE

# Proxyログを確認
kubectl logs POD_NAME -c cloudsql-proxy
```

**関連ファイル**: `docs/development-logs/service-recovery.txt`

### Redis接続エラー

**問題**: Redisへの接続タイムアウトまたは認証失敗

**解決策**:
1. Redisサービスが稼働しているか確認:
   ```bash
   kubectl get svc redis-service
   ```

2. Secretに保存されているRedis認証情報を確認:
   ```bash
   kubectl get secret redis-secret -o yaml
   ```

3. core-apiの環境変数で接続文字列を更新

---

## AIサービス

### Gemini API安全フィルター問題

**問題**: AIアドバイザーが空のレスポンスを返す、または`finish_reason=2` (SAFETY)エラー

**エラー**:
```python
finish_reason: FinishReason.SAFETY
```

**原因**:
- Gemini APIの安全フィルターがビジネス用語を誤検出
- デフォルトのハームカテゴリ閾値が過剰に厳格

**解決策**:

1. `services/ai-advisor/app/llm_advisor.py`で安全設定を構成:
   ```python
   from google.generativeai.types import HarmCategory, HarmBlockThreshold

   safety_settings = {
       HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
       HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
       HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
       HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
   }

   response = model.generate_content(
       prompt,
       generation_config=generation_config,
       safety_settings=safety_settings
   )
   ```

2. プロンプトで中立的な表現を使用:
   - 変更前: "経営改善のアドバイス"
   - 変更後: "運営に役立つ提案"

3. 箇条書きではなく自然な会話形式でプロンプトをフォーマット

**検証方法**:
```bash
# ai-advisorログで成功レスポンスを確認
kubectl logs -l app=ai-advisor | grep "finish_reason"

# 表示されるべき内容: finish_reason: FinishReason.STOP (SAFETYではない)
```

**関連ファイル**: `docs/development-logs/2025-10-10-changes.txt`

---

## Kubernetes・ネットワーク

### サービス名解決の失敗

**問題**: core-apiからai-advisorを呼び出す際に`Name or service not known`エラー

**エラー**:
```
httpx.ConnectError: [Errno -2] Name or service not known
```

**原因**:
- コードとKubernetesサービス定義の間でサービス名が不一致
- コードは`ai-advisor`を参照しているが、サービス名は`ai-advisor-service`

**解決策**:

1. ファイル間で一貫した命名を確保:

   **services/core-api/app/routers/analysis.py**:
   ```python
   AI_ADVISOR_URL = "http://ai-advisor-service:8002"
   ```

   **kubernetes/base/ai-advisor-service.yaml**:
   ```yaml
   metadata:
     name: ai-advisor-service
   ```

2. サービスディスカバリを検証:
   ```bash
   # Pod内から確認
   kubectl exec -it CORE_API_POD -- nslookup ai-advisor-service
   ```

**関連ファイル**: `docs/development-logs/2025-10-10-changes.txt`

### ImagePullBackOffエラー

**問題**: PodがImagePullBackOff状態で停止

**よくある原因**:
1. コンテナレジストリにイメージが存在しない
2. デプロイメントのイメージタグが間違っている
3. GKEにレジストリからのpull権限がない

**解決策**:
```bash
# 1. イメージが存在するか確認
gcloud artifacts docker images list \
  asia-northeast1-docker.pkg.dev/PROJECT_ID/REPO

# 2. デプロイメントのイメージ参照を確認
kubectl describe deployment DEPLOYMENT_NAME | grep Image

# 3. GKEにpull権限を付与
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

---

## フロントエンド・API連携

### CORSエラー

**問題**: ブラウザがCORSエラーでAPIリクエストをブロック

**解決策**:

`services/core-api/app/main.py`でCORSオリジンを更新:
```python
origins = [
    "http://localhost:3000",  # ローカル開発環境
    "https://your-domain.com",  # 本番環境
    "https://YOUR_FRONTEND_URL",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### APIエンドポイント変更

**問題**: フロントエンドが古いAPIエンドポイントを呼び出す

**よくある問題**:
- POSTとGETメソッドの不一致
- エンドポイントパスの変更

**修正例**（AIアドバイザー）:
```typescript
// 修正前
const response = await fetch('/api/ai-advice/generate', {
  method: 'POST',
  body: JSON.stringify(data)
});

// 修正後
const response = await fetch('/api/analysis/ai-advice', {
  method: 'GET'
});
```

**関連ファイル**: `docs/development-logs/2025-10-10-changes.txt`

---

## 一般的なデバッグ手順

### Pod状態の確認
```bash
kubectl get pods -n NAMESPACE
kubectl describe pod POD_NAME
kubectl logs POD_NAME [-c CONTAINER_NAME]
kubectl logs POD_NAME --previous  # 前回のコンテナログ
```

### SecretとConfigMapの検証
```bash
kubectl get secrets
kubectl get secret SECRET_NAME -o yaml
kubectl get configmaps
kubectl describe configmap CONFIGMAP_NAME
```

### サービス接続テスト
```bash
# ローカルマシンにポートフォワード
kubectl port-forward svc/SERVICE_NAME LOCAL_PORT:REMOTE_PORT

# エンドポイントをテスト
curl http://localhost:LOCAL_PORT/health
```

### データベースデバッグ
```bash
# データベースに接続
kubectl port-forward svc/postgres 5432:5432
psql -h localhost -U USER -d DATABASE

# テーブル確認
\dt
\d TABLE_NAME
```

---

## 予防のためのベストプラクティス

1. **依存関係のバージョン固定**: 重要なライブラリ（bcrypt、passlibなど）は正確なバージョンを指定
2. **環境の同一性**: 開発、ステージング、本番環境を同一に保つ
3. **包括的なログ記録**: 認証、API呼び出し、データベース操作に詳細なログを追加
4. **ヘルスチェック**: すべてのサービスで`/health`エンドポイントを実装
5. **モニタリング**: エラー率、API障害、認証問題のアラートを設定
6. **ドキュメント更新**: 新しい問題が発見されるたびにこのガイドを更新

---

## 関連リソース

- 開発ログ: `docs/development-logs/`
- アーキテクチャ概要: `docs/ARCHITECTURE.md`
- サービス復旧マニュアル: `docs/development-logs/service-recovery.txt`
- プロジェクト概要: `docs/PROJECT_OVERVIEW.md`
