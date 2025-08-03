from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from google.cloud import storage
import uuid
import requests

from .. import crud, schemas, security
from ..database import get_db
from ..gamification import PointCalculationEngine, BadgeEvaluationEngine
from ..security.rate_limit import limiter, RateLimits
from datetime import datetime

router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
)

# GCS設定
BUCKET_NAME = "your-gcp-project-id-receipts"
storage_client = storage.Client()

# OCR Processorサービスのエンドポイント
OCR_PROCESSOR_URL = "http://ocr-processor/process-gcs/"

@router.post("/upload", response_model=schemas.ReceiptUploadResponse)
@limiter.limit(RateLimits.UPLOAD)
async def upload_receipt(
    request: Request,
    db: Session = Depends(get_db), 
    file: UploadFile = File(...),
    token_data: schemas.TokenData = Depends(security.get_current_user)
):
    current_user = crud.get_user_by_email(db, email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. GCSにファイルをアップロード
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob_name = f"receipts/{uuid.uuid4()}-{file.filename}"
        blob = bucket.blob(blob_name)
        
        contents = await file.read()
        blob.upload_from_string(contents, content_type=file.content_type)
        
        gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCS upload failed: {str(e)}")

    # 2. OCRサービスを呼び出す
    try:
        response = requests.post(OCR_PROCESSOR_URL, json={"gcs_uri": gcs_uri})
        response.raise_for_status()
        ocr_result = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to call OCR service: {str(e)}")

    # 3. 重複チェック
    point_engine = PointCalculationEngine(db)
    receipt_info = {
        "supplier_name": ocr_result.get("supplier_name"),
        "total_amount": ocr_result.get("total_amount"),
        "receipt_date": datetime.now()
    }
    
    if point_engine.is_duplicate_receipt(receipt_info, current_user.id):
        raise HTTPException(
            status_code=400, 
            detail="このレシートは既にアップロード済みです"
        )
    
    # 4. 結果をDBに保存
    receipt_data = schemas.ReceiptCreate(
        supplier_name=ocr_result.get("supplier_name"),
        total_amount=ocr_result.get("total_amount"),
        image_gcs_path=gcs_uri,
        ocr_raw_data=ocr_result,
        items=[schemas.ReceiptItemCreate(**item) for item in ocr_result.get("line_items", [])]
    )
    
    db_receipt = crud.create_receipt(db=db, receipt=receipt_data, user_id=current_user.id)
    
    # 5. ポイント計算と付与
    try:
        upload_context = {
            "upload_time": datetime.now(),
            "weather_code": None  # TODO: 現在の天候情報を取得
        }
        
        point_result = point_engine.calculate_points(
            receipt_info, 
            current_user.id, 
            upload_context
        )
        
        # ポイント付与
        if point_result.total_points > 0:
            crud.update_user_points(
                db,
                current_user.id,
                point_result.total_points,
                "earn",
                f"レシートアップロード: {receipt_info.get('supplier_name', '不明')}",
                {
                    "receipt_id": db_receipt.id,
                    "base_points": point_result.base_points,
                    "bonus_points": point_result.bonus_points,
                    "bonus_details": point_result.bonus_details
                }
            )
        
        # 6. バッジ判定と授与
        badge_engine = BadgeEvaluationEngine(db)
        awarded_badges = badge_engine.evaluate_and_award_badges(current_user.id)
        
        # 7. レスポンスに追加情報を含める
        return {
            "receipt": db_receipt,
            "points_earned": point_result.total_points,
            "point_details": {
                "base_points": point_result.base_points,
                "bonus_points": point_result.bonus_points,
                "bonus_details": point_result.bonus_details
            },
            "badges_awarded": [{
                "badge_id": badge.badge_id,
                "badge_name": badge.badge_name,
                "is_new": badge.is_new
            } for badge in awarded_badges]
        }
        
    except Exception as e:
        # ポイント・バッジ処理でエラーが発生してもレシート保存は成功とする
        print(f"ポイント/バッジ処理エラー: {e}")
        return {
            "receipt": db_receipt,
            "points_earned": 0,
            "point_details": {
                "base_points": 0,
                "bonus_points": 0,
                "bonus_details": []
            },
            "badges_awarded": []
        }
