from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from .. import crud, models, schemas
from ..database import get_db
from .. import security

router = APIRouter(prefix="/api/line", tags=["line_integration"])

@router.post("/link")
def link_line_account(
    line_user_id: str,
    line_display_name: str = None,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーアカウントとLINEアカウントを連携
    """
    # 既に連携済みかチェック
    existing_integration = crud.get_line_integration_by_user(db, current_user.id)
    if existing_integration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既にLINEアカウントと連携済みです"
        )
    
    # 同じLINE IDが他のユーザーと連携済みかチェック
    existing_line = crud.get_line_integration_by_line_id(db, line_user_id)
    if existing_line:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このLINEアカウントは既に他のユーザーと連携されています"
        )
    
    # LINE連携を作成
    line_integration = schemas.LineIntegrationCreate(
        user_id=current_user.id,
        line_user_id=line_user_id,
        line_display_name=line_display_name
    )
    
    integration = crud.create_line_integration(db, line_integration)
    
    return {
        "message": "LINEアカウントとの連携が完了しました",
        "integration_id": integration.id
    }

@router.get("/status")
def get_line_integration_status(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーのLINE連携状況を取得
    """
    integration = crud.get_line_integration_by_user(db, current_user.id)
    
    if not integration:
        return {
            "is_linked": False,
            "message": "LINEアカウントと連携されていません"
        }
    
    return {
        "is_linked": True,
        "line_display_name": integration.line_display_name,
        "linked_at": integration.linked_at,
        "is_active": integration.is_active
    }

@router.delete("/unlink")
def unlink_line_account(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    LINEアカウントとの連携を解除
    """
    integration = crud.get_line_integration_by_user(db, current_user.id)
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LINEアカウントとの連携が見つかりません"
        )
    
    # 連携を無効化（削除ではなく無効化）
    integration.is_active = False
    db.commit()
    
    return {"message": "LINEアカウントとの連携を解除しました"}

# LINE Webhook関連
@router.post("/webhook")
async def line_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    LINE Messaging APIからのWebhookを処理
    """
    try:
        body = await request.body()
        # TODO: LINE署名検証を実装
        
        # Webhookペイロードを解析
        import json
        webhook_data = json.loads(body)
        
        # イベント処理
        for event in webhook_data.get("events", []):
            if event["type"] == "message":
                await handle_line_message(event, db)
            elif event["type"] == "follow":
                await handle_line_follow(event, db)
            elif event["type"] == "unfollow":
                await handle_line_unfollow(event, db)
        
        return {"status": "ok"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook処理でエラーが発生しました: {str(e)}"
        )

async def handle_line_message(event: Dict[str, Any], db: Session):
    """
    LINEメッセージイベントを処理
    """
    line_user_id = event["source"]["userId"]
    message_text = event["message"]["text"]
    
    # ユーザーの連携情報を取得
    integration = crud.get_line_integration_by_line_id(db, line_user_id)
    
    if integration:
        # 連携済みユーザーの場合の処理
        # TODO: メッセージに応じた処理を実装
        # 例: "ポイント確認" -> ポイント残高を返す
        # 例: "イベント情報" -> 最新イベントを返す
        pass
    else:
        # 未連携ユーザーの場合、連携方法を案内
        # TODO: LINE Messaging APIで返信メッセージを送信
        pass

async def handle_line_follow(event: Dict[str, Any], db: Session):
    """
    LINEフォローイベントを処理
    """
    line_user_id = event["source"]["userId"]
    # TODO: フォロー時の歓迎メッセージを送信
    pass

async def handle_line_unfollow(event: Dict[str, Any], db: Session):
    """
    LINEアンフォローイベントを処理
    """
    line_user_id = event["source"]["userId"]
    
    # 連携情報を無効化
    integration = crud.get_line_integration_by_line_id(db, line_user_id)
    if integration:
        integration.is_active = False
        db.commit()

# 管理者用: LINEメッセージ送信
@router.post("/admin/send-message")
def send_line_message(
    user_id: int,
    message: str,
    db: Session = Depends(get_db)
    # TODO: 管理者権限チェックを実装
):
    """
    特定のユーザーにLINEメッセージを送信（管理者用）
    """
    integration = crud.get_line_integration_by_user(db, user_id)
    
    if not integration or not integration.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーのLINE連携が見つかりません"
        )
    
    # TODO: LINE Messaging APIでメッセージを送信
    # line_bot_api.push_message(integration.line_user_id, TextSendMessage(text=message))
    
    return {"message": "メッセージを送信しました"}