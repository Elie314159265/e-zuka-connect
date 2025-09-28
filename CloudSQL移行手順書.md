# CloudSQL(PostgreSQL)移行手順書

## 概要
現在StatefulSetで運用しているPostgreSQLデータベースをGoogle Cloud SQLのPostgreSQLインスタンスに移行し、データの安全性と可用性を向上させます。

## 現在の構成
- **データベース**: PostgreSQL 13 (StatefulSet)
- **ストレージ**: 20Gi PersistentVolumeClaim
- **接続先**: `postgresql-service:5432`
- **認証情報**: ConfigMapで管理 (user/password/dbname)

## 移行の利点
- **高可用性**: 自動バックアップ・レプリケーション
- **データ保護**: ポイントインタイム復旧
- **運用負荷軽減**: マネージドサービス
- **スケーラビリティ**: 必要に応じた性能調整

## 前提条件
- GCPプロジェクトの準備
- Cloud SQL Admin APIの有効化
- 適切なIAM権限の設定
- データベースダウンタイムの調整

## 移行手順

### Phase 1: CloudSQL インスタンスの作成

#### 1.1 CloudSQL インスタンスの作成
```bash
# Cloud SQL インスタンスを作成
gcloud sql instances create your-gcp-project-id-db \
    --database-version=POSTGRES_13 \
    --cpu=1 \
    --memory=3840MB \
    --region=asia-northeast1 \
    --storage-type=SSD \
    --storage-size=20GB \
    --storage-auto-increase \
    --backup-start-time=03:00 \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=04 \
    --maintenance-release-channel=production
```

#### 1.2 データベースとユーザーの作成
```bash
# データベースを作成
gcloud sql databases create dbname \
    --instance=your-gcp-project-id-db

# ユーザーを作成
gcloud sql users create user \
    --instance=your-gcp-project-id-db \
    --password=your-secure-password
```

#### 1.3 ネットワーク設定
```bash
# プライベートIP設定（推奨）
gcloud sql instances patch your-gcp-project-id-db \
    --network=projects/YOUR_PROJECT_ID/global/networks/default \
    --no-assign-ip
```

### Phase 2: データ移行

#### 2.1 現在のデータのバックアップ
```bash
# 現在のPodに接続してデータをダンプ
kubectl exec -n your-gcp-project-id postgresql-0 -- pg_dump \
    -U user -d dbname --clean --no-owner --no-privileges \
    > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 2.2 CloudSQLへのデータ復元
```bash
# Cloud SQL Proxyを使用してローカルから接続
cloud_sql_proxy -instances=YOUR_PROJECT_ID:asia-northeast1:your-gcp-project-id-db=tcp:5433 &

# データを復元
psql -h localhost -p 5433 -U user -d dbname < backup_YYYYMMDD_HHMMSS.sql
```

### Phase 3: アプリケーション設定の更新

#### 3.1 Secretの作成
```yaml
# cloudsql-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudsql-secret
  namespace: your-gcp-project-id
type: Opaque
data:
  username: dXNlcg==  # base64 encoded "user"
  password: WU9VUl9TRUNSRVRFX1BBU1NXT1JE  # base64 encoded password
```

#### 3.2 ConfigMapの更新
```yaml
# kubernetes/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: your-gcp-project-id
data:
  # General App Settings
  GINSENG_MODE: "production"
  LOG_LEVEL: "info"

  # Core API Database Settings (CloudSQL)
  DB_NAME: "dbname"
  DB_HOST: "127.0.0.1"  # Cloud SQL Proxyを使用
  DB_PORT: "5432"

  # Core API JWT Settings
  JWT_SECRET_KEY: "your-secret-key-here-change-this-in-production"
```

#### 3.3 Core API Deploymentの更新
```yaml
# kubernetes/base/core-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: core-api
  namespace: your-gcp-project-id
spec:
  replicas: 1
  selector:
    matchLabels:
      app: core-api
  template:
    metadata:
      labels:
        app: core-api
    spec:
      containers:
      - name: core-api
        image: asia-northeast1-docker.pkg.dev/your-gcp-project-id/your-gcp-project-id-repo/core-api:v1.3.5-analysis-fix
        ports:
        - containerPort: 80
        startupProbe:
          httpGet:
            path: /api
            port: 80
          failureThreshold: 30
          periodSeconds: 10
          initialDelaySeconds: 30
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DEBUG_MODE
          value: "false"
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: "/var/secrets/google/gcp-credentials.json"
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: cloudsql-secret
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: cloudsql-secret
              key: password
        envFrom:
        - configMapRef:
            name: app-config
        volumeMounts:
        - name: google-cloud-key
          mountPath: /var/secrets/google
          readOnly: true
      # Cloud SQL Proxy サイドカー
      - name: cloudsql-proxy
        image: gcr.io/cloudsql-docker/gce-proxy:1.33.2
        command:
          - "/cloud_sql_proxy"
          - "-instances=YOUR_PROJECT_ID:asia-northeast1:your-gcp-project-id-db=tcp:5432"
          - "-credential_file=/var/secrets/google/gcp-credentials.json"
        volumeMounts:
        - name: google-cloud-key
          mountPath: /var/secrets/google
          readOnly: true
        securityContext:
          runAsNonRoot: true
      volumes:
      - name: google-cloud-key
        secret:
          secretName: gcp-ocr-credentials
```

### Phase 4: 移行実行

#### 4.1 メンテナンスモードの開始
```bash
# フロントエンドをメンテナンスページに切り替え
kubectl scale deployment frontend --replicas=0 -n your-gcp-project-id
```

#### 4.2 データベース接続の停止
```bash
# Core APIを停止
kubectl scale deployment core-api --replicas=0 -n your-gcp-project-id
```

#### 4.3 最終データ同期
```bash
# 最新のデータをバックアップして CloudSQL に反映
kubectl exec -n your-gcp-project-id postgresql-0 -- pg_dump \
    -U user -d dbname --clean --no-owner --no-privileges \
    > final_backup_$(date +%Y%m%d_%H%M%S).sql

# CloudSQL に復元
psql -h localhost -p 5433 -U user -d dbname < final_backup_YYYYMMDD_HHMMSS.sql
```

#### 4.4 新しい設定でアプリケーションを起動
```bash
# Secret を作成
kubectl apply -f cloudsql-secret.yaml

# ConfigMap と Deployment を更新
kubectl apply -f kubernetes/base/configmap.yaml
kubectl apply -f kubernetes/base/core-api-deployment.yaml

# サービスを再開
kubectl scale deployment core-api --replicas=1 -n your-gcp-project-id
kubectl scale deployment frontend --replicas=1 -n your-gcp-project-id
```

### Phase 5: 旧リソースのクリーンアップ

#### 5.1 動作確認後の旧PostgreSQL削除
```bash
# StatefulSet を削除
kubectl delete statefulset postgresql -n your-gcp-project-id

# Service を削除
kubectl delete service postgresql-service -n your-gcp-project-id

# PVC を削除（データは事前にバックアップ済み）
kubectl delete pvc postgres-storage-postgresql-0 -n your-gcp-project-id
```

## 動作確認項目
- [ ] CloudSQL インスタンスへの接続確認
- [ ] アプリケーションの正常起動
- [ ] ユーザー認証の動作確認
- [ ] レシート登録・取得の動作確認
- [ ] データ整合性の確認

## ロールバック手順
移行に問題が発生した場合：

1. Core API を旧設定に戻す
2. PostgreSQL StatefulSet を再デプロイ
3. バックアップデータを復元
4. サービスを再開

## セキュリティ考慮事項
- Cloud SQL Proxy を使用した暗号化通信
- 認証情報のSecret管理
- ネットワークレベルでのアクセス制御
- 定期バックアップの設定

## 運用上の注意点
- CloudSQL の料金体系を確認
- バックアップ・復旧手順の文書化
- モニタリング設定の追加
- ログ監視の設定