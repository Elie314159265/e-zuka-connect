import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, auth, receipts, weather, historical_weather, debug, analysis, gamification, stores, line_integration, products
from .security.rate_limit import setup_rate_limiting
from .logging_config import setup_logging

# ログの初期化
setup_logging()

# 環境変数を取得
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

app = FastAPI(
    title="E-Zuka Connect API",
    description="Local commerce gamification platform",
    version="1.0.0",
    docs_url="/docs" if DEBUG_MODE else None,  # 本番環境でSwagger UI無効化
    redoc_url="/redoc" if DEBUG_MODE else None,  # 本番環境でReDoc無効化
)

# レート制限のセットアップ
setup_rate_limiting(app)

origins = [
    "https://your-gcp-project-id.com",
    ##"http://your-gcp-project-id.com",
    "https://3000-cs-e10ba524-0313-401b-9374-ba2fd723a109.cs-asia-east1-cats.cloudshell.dev",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基本的なAPIルーター
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(receipts.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(historical_weather.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(gamification.router)
app.include_router(stores.router)
app.include_router(line_integration.router)
app.include_router(products.router)

# デバッグエンドポイントは開発環境またはDEBUG_MODEが有効な場合のみ
if DEBUG_MODE or ENVIRONMENT in ["development", "testing"]:
    app.include_router(debug.router, prefix="/api")
    print(f"⚠️  DEBUG MODE ENABLED - Debug endpoints are accessible at /api/debug/*")

@app.get("/api")
def read_root():
    return {"status": "ok"}
