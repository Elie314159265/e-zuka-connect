from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, models, schemas
from ..database import get_db
from ..security.auth import get_current_store_owner

router = APIRouter(prefix="/api/promotions", tags=["promotions"])

# ========== 事業者向けプロモーション管理 ==========

@router.post("/", response_model=schemas.Promotion)
def create_promotion(
    promotion_data: schemas.PromotionBase,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーションを作成"""
    # 商品が指定されている場合、店舗所有権を確認
    product = crud.get_product(db=db, product_id=promotion_data.product_id)
    if not product or product.store_id != current_owner.store_id:
        raise HTTPException(status_code=400, detail="指定された商品が無効です")

    # オーナーの店舗IDを含む新しいオブジェクトを作成
    promotion = schemas.PromotionCreate(
        **promotion_data.model_dump(),
        store_id=current_owner.store_id
    )

    # デフォルトでscheduledステータスを設定
    db_promotion = models.Promotion(**promotion.model_dump(), status="scheduled")
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)

    return db_promotion

@router.get("/", response_model=List[schemas.Promotion])
def get_promotions(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーション一覧を取得"""
    return crud.get_promotions(
        db=db,
        store_id=current_owner.store_id,
        status=status,
        skip=skip,
        limit=limit
    )

@router.get("/{promotion_id}", response_model=schemas.Promotion)
def get_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーションを取得"""
    promotion = crud.get_promotion(db=db, promotion_id=promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="プロモーションが見つかりません")

    # 店舗の所有権確認
    if promotion.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    return promotion

@router.put("/{promotion_id}", response_model=schemas.Promotion)
def update_promotion(
    promotion_id: int,
    promotion_update: schemas.PromotionUpdate,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーションを更新"""
    # 既存プロモーションを確認
    existing_promotion = crud.get_promotion(db=db, promotion_id=promotion_id)
    if not existing_promotion:
        raise HTTPException(status_code=404, detail="プロモーションが見つかりません")

    # 店舗の所有権確認
    if existing_promotion.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    # 商品が変更される場合、店舗所有権を確認
    if promotion_update.product_id is not None:
        if promotion_update.product_id != existing_promotion.product_id:
            product = crud.get_product(db=db, product_id=promotion_update.product_id)
            if not product or product.store_id != current_owner.store_id:
                raise HTTPException(status_code=400, detail="指定された商品が無効です")

    updated_promotion = crud.update_promotion(
        db=db, promotion_id=promotion_id, promotion_update=promotion_update
    )
    return updated_promotion

@router.delete("/{promotion_id}")
def delete_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーションを削除"""
    # 既存プロモーションを確認
    existing_promotion = crud.get_promotion(db=db, promotion_id=promotion_id)
    if not existing_promotion:
        raise HTTPException(status_code=404, detail="プロモーションが見つかりません")

    # 店舗の所有権確認
    if existing_promotion.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    success = crud.delete_promotion(db=db, promotion_id=promotion_id)
    if not success:
        raise HTTPException(status_code=400, detail="プロモーションの削除に失敗しました")

    return {"message": "プロモーションを削除しました"}

@router.post("/{promotion_id}/publish", response_model=schemas.Promotion)
def publish_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """プロモーションを手動で公開する"""
    # 既存プロモーションを確認
    existing_promotion = crud.get_promotion(db=db, promotion_id=promotion_id)
    if not existing_promotion:
        raise HTTPException(status_code=404, detail="プロモーションが見つかりません")

    # 店舗の所有権確認
    if existing_promotion.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    # 公開処理
    published_promotion = crud.publish_promotion(db=db, promotion_id=promotion_id)
    return published_promotion

# ========== ユーザー向けプロモーション表示 ==========

@router.get("/public/active", response_model=List[schemas.Promotion])
def get_active_promotions(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """アクティブなプロモーション一覧を取得（ユーザー向け・認証不要）"""
    promotions = crud.get_active_promotions(db=db, limit=limit)

    # 閲覧数をインクリメント（簡易的な実装）
    for promotion in promotions:
        crud.increment_promotion_views(db=db, promotion_id=promotion.id)

    return promotions
