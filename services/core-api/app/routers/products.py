from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, models, schemas
from ..database import get_db
from ..security.auth import get_current_store_owner

router = APIRouter(prefix="/api/products", tags=["products"])

# ========== 商品カテゴリ管理 ==========

@router.post("/categories", response_model=schemas.ProductCategory)
def create_product_category(
    category_data: schemas.ProductCategoryBase,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品カテゴリを作成"""
    # オーナーの店舗IDを含む新しいオブジェクトを作成
    category = schemas.ProductCategoryCreate(
        **category_data.model_dump(),
        store_id=current_owner.store_id
    )
    return crud.create_product_category(db=db, category=category)

@router.get("/categories", response_model=List[schemas.ProductCategory])
def get_product_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品カテゴリ一覧を取得"""
    return crud.get_product_categories(
        db=db, store_id=current_owner.store_id, skip=skip, limit=limit
    )

@router.get("/categories/{category_id}", response_model=schemas.ProductCategory)
def get_product_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品カテゴリを取得"""
    category = crud.get_product_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")

    # 店舗の所有権確認
    if category.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    return category

@router.put("/categories/{category_id}", response_model=schemas.ProductCategory)
def update_product_category(
    category_id: int,
    category_update: schemas.ProductCategoryUpdate,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品カテゴリを更新"""
    # 既存カテゴリを確認
    existing_category = crud.get_product_category(db=db, category_id=category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")

    # 店舗の所有権確認
    if existing_category.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    updated_category = crud.update_product_category(
        db=db, category_id=category_id, category_update=category_update
    )
    return updated_category

@router.delete("/categories/{category_id}")
def delete_product_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品カテゴリを削除"""
    # 既存カテゴリを確認
    existing_category = crud.get_product_category(db=db, category_id=category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")

    # 店舗の所有権確認
    if existing_category.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    success = crud.delete_product_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=400, detail="カテゴリの削除に失敗しました")

    return {"message": "カテゴリを削除しました"}

# ========== 商品管理 ==========

@router.post("/", response_model=schemas.Product)
def create_product(
    product_data: schemas.ProductBase,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品を作成"""
    # カテゴリが指定されている場合、店舗所有権を確認
    if product_data.category_id:
        category = crud.get_product_category(db=db, category_id=product_data.category_id)
        if not category or category.store_id != current_owner.store_id:
            raise HTTPException(status_code=400, detail="指定されたカテゴリが無効です")

    # 商品コードの重複確認
    if product_data.product_code:
        existing = crud.get_product_by_code(
            db=db, store_id=current_owner.store_id, product_code=product_data.product_code
        )
        if existing:
            raise HTTPException(status_code=400, detail="商品コードが既に存在します")

    # オーナーの店舗IDを含む新しいオブジェクトを作成
    product = schemas.ProductCreate(
        **product_data.model_dump(),
        store_id=current_owner.store_id
    )
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.Product])
def get_products(
    category_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品一覧を取得"""
    return crud.get_products(
        db=db,
        store_id=current_owner.store_id,
        category_id=category_id,
        is_active=is_active,
        skip=skip,
        limit=limit
    )

@router.get("/search", response_model=List[schemas.Product])
def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品を検索"""
    return crud.search_products(
        db=db,
        store_id=current_owner.store_id,
        search_query=q,
        skip=skip,
        limit=limit
    )

@router.get("/featured", response_model=List[schemas.Product])
def get_featured_products(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """おすすめ商品を取得"""
    return crud.get_featured_products(
        db=db, store_id=current_owner.store_id, limit=limit
    )

@router.get("/seasonal", response_model=List[schemas.Product])
def get_seasonal_products(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """季節商品を取得"""
    return crud.get_seasonal_products(
        db=db, store_id=current_owner.store_id, limit=limit
    )

@router.get("/low-stock", response_model=List[schemas.Product])
def get_low_stock_products(
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """在庫が少ない商品を取得"""
    return crud.get_low_stock_products(db=db, store_id=current_owner.store_id)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品を取得"""
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    # 店舗の所有権確認
    if product.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    return product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品を更新"""
    # 既存商品を確認
    existing_product = crud.get_product(db=db, product_id=product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    # 店舗の所有権確認
    if existing_product.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    # カテゴリが変更される場合、店舗所有権を確認
    if product_update.category_id is not None:
        if product_update.category_id != existing_product.category_id:
            category = crud.get_product_category(db=db, category_id=product_update.category_id)
            if not category or category.store_id != current_owner.store_id:
                raise HTTPException(status_code=400, detail="指定されたカテゴリが無効です")

    # 商品コードが変更される場合、重複確認
    if product_update.product_code is not None:
        if product_update.product_code != existing_product.product_code:
            existing = crud.get_product_by_code(
                db=db, store_id=current_owner.store_id, product_code=product_update.product_code
            )
            if existing and existing.id != product_id:
                raise HTTPException(status_code=400, detail="商品コードが既に存在します")

    updated_product = crud.update_product(
        db=db, product_id=product_id, product_update=product_update
    )
    return updated_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品を削除"""
    # 既存商品を確認
    existing_product = crud.get_product(db=db, product_id=product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    # 店舗の所有権確認
    if existing_product.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    success = crud.delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=400, detail="商品の削除に失敗しました")

    return {"message": "商品を削除しました"}

# ========== 在庫管理 ==========

@router.put("/{product_id}/stock", response_model=schemas.Product)
def update_product_stock(
    product_id: int,
    stock_update: schemas.ProductStockUpdate,
    db: Session = Depends(get_db),
    current_owner: models.StoreOwner = Depends(get_current_store_owner)
):
    """商品在庫を更新"""
    # 既存商品を確認
    existing_product = crud.get_product(db=db, product_id=product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    # 店舗の所有権確認
    if existing_product.store_id != current_owner.store_id:
        raise HTTPException(status_code=403, detail="アクセス権限がありません")

    try:
        updated_product = crud.update_product_stock(
            db=db,
            product_id=product_id,
            quantity_change=stock_update.quantity_change,
            reason=stock_update.reason
        )
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))