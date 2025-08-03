from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from .. import security

router = APIRouter(prefix="/api/gamification", tags=["gamification"])

@router.get("/profile", response_model=schemas.GamificationProfile)
def get_user_gamification_profile(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーのゲーミフィケーションプロファイルを取得
    """
    profile = crud.get_gamification_profile(db, current_user.id)
    if not profile:
        # プロファイルが存在しない場合は作成
        profile = crud.create_gamification_profile(db, current_user.id)
    
    return profile

@router.get("/badges", response_model=List[schemas.UserBadge])
def get_user_badges(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーが獲得したバッジ一覧を取得
    """
    return crud.get_user_badges(db, current_user.id)

@router.post("/points/earn")
def earn_points(
    points: int,
    description: str,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    ポイントを獲得する（レシートアップロード等で使用）
    """
    profile = crud.update_user_points(
        db, 
        current_user.id, 
        points, 
        "earn", 
        description,
        {"action": "manual_earn"}
    )
    
    return {"message": f"{points}ポイント獲得しました", "current_points": profile.contribution_points}

@router.post("/points/redeem")
def redeem_points(
    points: int,
    description: str,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    ポイントを使用する（クーポン交換等で使用）
    """
    profile = crud.get_gamification_profile(db, current_user.id)
    if not profile or profile.contribution_points < points:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ポイントが不足しています"
        )
    
    profile = crud.update_user_points(
        db, 
        current_user.id, 
        points, 
        "redeem", 
        description,
        {"action": "manual_redeem"}
    )
    
    return {"message": f"{points}ポイント使用しました", "current_points": profile.contribution_points}

# ========== 特典交換機能 ==========

@router.get("/rewards", response_model=List[schemas.Reward])
def get_available_rewards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    利用可能な特典一覧を取得
    """
    return crud.get_rewards(db, skip=skip, limit=limit, is_active=True)

@router.post("/redeem")
def redeem_reward(
    reward_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    特典を交換する
    """
    try:
        user_reward = crud.redeem_reward(db, current_user.id, reward_id)
        
        return {
            "message": "特典の交換が完了しました",
            "coupon_code": user_reward.coupon_code,
            "expires_at": user_reward.expires_at,
            "reward_title": user_reward.reward.title,
            "remaining_points": crud.get_gamification_profile(db, current_user.id).contribution_points
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"特典交換でエラーが発生しました: {str(e)}"
        )

@router.get("/my-rewards", response_model=List[schemas.UserReward])
def get_my_rewards(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    自分の特典交換履歴を取得
    """
    return crud.get_user_rewards(db, current_user.id, skip=skip, limit=limit)

# 管理者用エンドポイント
@router.post("/admin/badges", response_model=schemas.Badge)
def create_badge(
    badge: schemas.BadgeCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    新しいバッジを作成（管理者のみ）
    """
    # TODO: 管理者権限チェックを実装
    return crud.create_badge(db, badge)

@router.post("/admin/award-badge")
def award_badge_to_user(
    user_id: int,
    badge_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    ユーザーにバッジを授与（管理者のみ）
    """
    # TODO: 管理者権限チェックを実装
    user_badge = crud.award_badge(db, user_id, badge_id)
    return {"message": "バッジを授与しました", "user_badge_id": user_badge.id}

@router.post("/admin/rewards", response_model=schemas.Reward)
def create_reward(
    reward: schemas.RewardCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    新しい特典を作成（管理者のみ）
    """
    # TODO: 管理者権限チェックを実装
    return crud.create_reward(db, reward)