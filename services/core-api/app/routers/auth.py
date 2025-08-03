from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, schemas, security
from ..database import get_db
from ..security.rate_limit import limiter, RateLimits
from ..logging_config import security_logger

router = APIRouter(
    prefix="/token",
    tags=["auth"],
)

@router.post("/", response_model=schemas.Token)
@limiter.limit(RateLimits.AUTH_STRICT)
def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user_by_email(db, email=form_data.username)
    client_ip = request.client.host if request.client else "unknown"
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # ログイン失敗をログに記録
        security_logger.login_attempt(
            email=form_data.username, 
            success=False, 
            ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ログイン成功をログに記録
    security_logger.login_attempt(
        email=user.email, 
        success=True, 
        ip_address=client_ip
    )
    
    access_token = security.create_access_token(data={"sub": user.email})
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.Token)
@limiter.limit(RateLimits.AUTH_STRICT)
def refresh_access_token(
    request: Request,
    token_refresh: schemas.TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    リフレッシュトークンを使用してアクセストークンを更新
    """
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        payload = security.verify_refresh_token(token_refresh.refresh_token)
        email = payload.get("sub")
        if not email:
            security_logger.token_refresh(email="unknown", success=False, ip_address=client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なトークンです"
            )
        
        # ユーザーの存在確認
        user = crud.get_user_by_email(db, email=email)
        if not user:
            security_logger.token_refresh(email=email, success=False, ip_address=client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザーが見つかりません"
            )
        
        # 成功をログに記録
        security_logger.token_refresh(email=user.email, success=True, ip_address=client_ip)
        
        # 新しいトークンペアを生成
        new_access_token = security.create_access_token(data={"sub": user.email})
        new_refresh_token = security.create_refresh_token(data={"sub": user.email})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        # 既にログ記録済みの場合は再発生
        raise e
    except Exception as e:
        # 予期しないエラーをログに記録
        security_logger.token_refresh(email="unknown", success=False, ip_address=client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンの更新に失敗しました"
        )
