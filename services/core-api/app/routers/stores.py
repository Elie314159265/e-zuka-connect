from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from .. import security
from ..security import rls
from ..security.password_validator import password_validator

router = APIRouter(prefix="/api/stores", tags=["stores"])

# ========== 一般ユーザー向けエンドポイント ==========

@router.get("/", response_model=List[schemas.Store])
def get_stores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    店舗一覧を取得（一般公開）
    """
    return crud.get_stores(db, skip=skip, limit=limit)

@router.get("/{store_id}", response_model=schemas.Store)
def get_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    """
    特定の店舗情報を取得
    """
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="店舗が見つかりません"
        )
    return store

@router.get("/{store_id}/events", response_model=List[schemas.Event])
def get_store_events(
    store_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    店舗のイベント一覧を取得
    """
    return crud.get_store_events(db, store_id, skip=skip, limit=limit)

@router.get("/{store_id}/archive", response_model=List[schemas.ArchiveContent])
def get_store_archive_contents(
    store_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    店舗のアーカイブコンテンツを取得（公開済みのもののみ）
    """
    return crud.get_public_archive_contents(db, skip=skip, limit=limit)

# ========== 事業者向けエンドポイント ==========

@router.post("/", response_model=schemas.Store)
def create_store(
    store: schemas.StoreCreate,
    db: Session = Depends(get_db)
    # TODO: 管理者権限チェックを実装
):
    """
    新しい店舗を作成（管理者のみ）
    """
    return crud.create_store(db, store)

# 店舗オーナー認証関連
@router.post("/owners/register", response_model=schemas.StoreOwner)
def register_store_owner(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    店舗オーナーアカウントを作成（店舗も同時に作成）
    """
    # パスワード強度チェック
    password_validator.validate_or_raise(request["password"])
    
    # 既存のメールアドレスチェック
    existing_owner = crud.get_store_owner_by_email(db, request["email"])
    if existing_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に登録されています"
        )
    
    # 店舗を作成
    store_data = schemas.StoreCreate(
        name=request["store_name"],
        business_type="一般店舗",
        email=request["email"]
    )
    store = crud.create_store(db, store_data)
    
    # 店舗オーナーを作成
    store_owner_data = schemas.StoreOwnerCreate(
        email=request["email"],
        password=request["password"],
        full_name=request["full_name"],
        store_id=store.id
    )
    
    return crud.create_store_owner(db, store_owner_data)

@router.post("/owners/login", response_model=schemas.Token)
def login_store_owner(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    店舗オーナーのログイン
    """
    store_owner = crud.get_store_owner_by_email(db, form_data.username)
    if not store_owner or not security.verify_password(form_data.password, store_owner.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": store_owner.email})
    refresh_token = security.create_refresh_token(data={"sub": store_owner.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/owners/refresh", response_model=schemas.Token)
def refresh_store_owner_token(
    token_refresh: schemas.TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Store Owner用リフレッシュトークンを使用してアクセストークンを更新
    """
    payload = security.verify_refresh_token(token_refresh.refresh_token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです"
        )
    
    # Store Ownerの存在確認
    store_owner = crud.get_store_owner_by_email(db, email=email)
    if not store_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Store Ownerが見つかりません"
        )
    
    # 新しいトークンペアを生成
    new_access_token = security.create_access_token(data={"sub": store_owner.email})
    new_refresh_token = security.create_refresh_token(data={"sub": store_owner.email})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

def get_current_store_owner(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    店舗オーナーの認証情報を取得
    """
    # JWTトークンをデコード
    payload = security.decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです"
        )
    
    # 店舗オーナーを取得
    store_owner = crud.get_store_owner_by_email(db, email)
    if store_owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="店舗オーナーが見つかりません"
        )
    
    # RLSのセッションコンテキストを設定
    rls.set_session_context(store_id=store_owner.store_id)
    
    return store_owner

# 店舗オーナー用ダッシュボードエンドポイント
@router.get("/dashboard/events", response_model=List[schemas.Event])
def get_my_store_events(
    skip: int = 0,
    limit: int = 100,
    current_owner: models.StoreOwner = Depends(get_current_store_owner),
    db: Session = Depends(get_db)
):
    """
    自分の店舗のイベント一覧を取得（店舗オーナー用）
    """
    return crud.get_store_events(db, current_owner.store_id, skip=skip, limit=limit)

@router.post("/dashboard/events", response_model=schemas.Event)
def create_store_event(
    event: schemas.EventCreate,
    current_owner: models.StoreOwner = Depends(get_current_store_owner),
    db: Session = Depends(get_db)
):
    """
    店舗イベントを作成（店舗オーナー用）
    """
    # store_idを現在のオーナーの店舗に設定
    event.store_id = current_owner.store_id
    return crud.create_event(db, event)

@router.get("/dashboard/archive", response_model=List[schemas.ArchiveContent])
def get_my_store_archive_contents(
    skip: int = 0,
    limit: int = 100,
    current_owner: models.StoreOwner = Depends(get_current_store_owner),
    db: Session = Depends(get_db)
):
    """
    自分の店舗のアーカイブコンテンツ一覧を取得（店舗オーナー用）
    """
    return crud.get_store_archive_contents(db, current_owner.store_id, skip=skip, limit=limit)

@router.post("/dashboard/archive", response_model=schemas.ArchiveContent)
def create_archive_content(
    content: schemas.ArchiveContentCreate,
    current_owner: models.StoreOwner = Depends(get_current_store_owner),
    db: Session = Depends(get_db)
):
    """
    アーカイブコンテンツを作成（店舗オーナー用）
    """
    # store_idを現在のオーナーの店舗に設定
    content.store_id = current_owner.store_id
    return crud.create_archive_content(db, content)