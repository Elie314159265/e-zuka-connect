import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import redis
from typing import Optional

# Redis設定
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # Redis接続テスト
    redis_client.ping()
except (redis.ConnectionError, redis.TimeoutError) as e:
    print(f"Redis connection failed: {e}")
    redis_client = None

# レート制限設定
def get_identifier(request: Request) -> str:
    """
    リクエストの識別子を取得
    認証されたユーザーの場合はユーザーID、そうでなければIPアドレス
    """
    # Authorization headerからユーザーを特定
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            from .. import security
            token = auth_header.split(" ")[1]
            payload = security.decode_token(token)
            user_email = payload.get("sub")
            if user_email:
                return f"user:{user_email}"
        except:
            pass
    
    # IPアドレスベースのレート制限
    return get_remote_address(request)

# Limiterインスタンスの作成
if redis_client is not None:
    limiter = Limiter(
        key_func=get_identifier,
        storage_uri=REDIS_URL,
        default_limits=["1000/day", "100/hour"]  # デフォルト制限
    )
else:
    # Redis接続失敗時はメモリベースのlimiter（開発・テスト用）
    limiter = Limiter(
        key_func=get_identifier,
        storage_uri="memory://",
        default_limits=["1000/day", "100/hour"]
    )

# レート制限エラーハンドラー
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    レート制限エラーのカスタムハンドラー
    """
    response = JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": f"レート制限に達しました。{exc.detail}",
            "retry_after": str(exc.retry_after) if exc.retry_after else None
        }
    )
    response.headers["X-RateLimit-Limit"] = str(exc.limit)
    response.headers["X-RateLimit-Remaining"] = str(exc.remaining)
    response.headers["X-RateLimit-Reset"] = str(exc.reset)
    return response

def setup_rate_limiting(app: FastAPI):
    """
    FastAPIアプリにレート制限を設定
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# 特定のエンドポイント用のレート制限デコレータ
class RateLimits:
    """
    よく使用されるレート制限パターン
    """
    # 認証関連（厳格）
    AUTH_STRICT = "5/minute"
    
    # 一般的なAPI（通常）
    API_NORMAL = "60/minute"
    
    # 高頻度API（緩い）
    API_FREQUENT = "300/minute"
    
    # 公開API（非常に厳格）
    PUBLIC_API = "20/minute"
    
    # アップロード系（厳格）
    UPLOAD = "10/minute"