"""
バッジ自動判定エンジン
ユーザーの活動に基づいてバッジを自動授与するシステム
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models, schemas, crud
import logging

logger = logging.getLogger(__name__)

class BadgeEvaluationEngine:
    """
    バッジ評価・自動授与エンジン
    ユーザーの活動データを分析し、新規獲得可能なバッジを判定・授与する
    """
    
    def __init__(self, db: Session):
        self.db = db
        
    def evaluate_and_award_badges(self, user_id: int) -> List[schemas.BadgeAwardResult]:
        """
        バッジ評価とのメイン処理
        
        Args:
            user_id: 評価対象のユーザーID
            
        Returns:
            List[BadgeAwardResult]: 授与されたバッジのリスト
        """
        try:
            awarded_badges = []
            
            # 現在のユーザー獲得バッジを取得
            existing_badges = self._get_user_badge_ids(user_id)
            
            # 各カテゴリのバッジを評価
            activity_badges = self._evaluate_activity_badges(user_id, existing_badges)
            awarded_badges.extend(activity_badges)
            
            consecutive_badges = self._evaluate_consecutive_badges(user_id, existing_badges)
            awarded_badges.extend(consecutive_badges)
            
            amount_badges = self._evaluate_amount_badges(user_id, existing_badges)
            awarded_badges.extend(amount_badges)
            
            return awarded_badges
            
        except Exception as e:
            logger.error(f"バッジ評価エラー: {e}")
            return []
    
    def _get_user_badge_ids(self, user_id: int) -> set:
        """ユーザーが既に獲得しているバッジIDのセットを取得"""
        try:
            profile = crud.get_gamification_profile(self.db, user_id)
            if not profile:
                return set()
            
            user_badges = self.db.query(models.UserBadge).filter(
                models.UserBadge.profile_id == profile.id
            ).all()
            
            return {badge.badge_id for badge in user_badges}
            
        except Exception as e:
            logger.error(f"ユーザーバッジ取得エラー: {e}")
            return set()
    
    def _evaluate_activity_badges(self, user_id: int, existing_badges: set) -> List[schemas.BadgeAwardResult]:
        """アクティビティ系バッジの評価"""
        awarded_badges = []
        
        try:
            # レシート総数を取得
            total_receipts = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id
            ).count()
            
            # 各レシート数バッジを評価
            receipt_milestones = [
                (1, "はじめの一歩", "初回レシートアップロード"),
                (10, "レシート10枚達成", "10枚のレシートをアップロードしました"),
                (50, "レシート50枚達成", "50枚のレシートをアップロードしました"),
                (100, "レシート100枚達成", "100枚のレシートをアップロードしました"),
                (500, "レシートマスター", "500枚のレシートをアップロードしました")
            ]
            
            for count, name, description in receipt_milestones:
                if total_receipts >= count:
                    badge = self._ensure_badge_exists(name, description, {
                        "type": "receipt_count",
                        "condition": ">=",
                        "value": count
                    })
                    
                    if badge and badge.id not in existing_badges:
                        result = self._award_badge_to_user(user_id, badge.id, badge.name)
                        if result:
                            awarded_badges.append(result)
            
            return awarded_badges
            
        except Exception as e:
            logger.error(f"アクティビティバッジ評価エラー: {e}")
            return []
    
    def _evaluate_consecutive_badges(self, user_id: int, existing_badges: set) -> List[schemas.BadgeAwardResult]:
        """連続利用系バッジの評価"""
        awarded_badges = []
        
        try:
            # 過去30日間のレシートを取得して連続日数を計算
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_receipts = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id,
                models.Receipt.created_at >= thirty_days_ago
            ).order_by(models.Receipt.created_at.desc()).all()
            
            consecutive_days = self._count_consecutive_days(recent_receipts)
            
            # 連続利用バッジを評価
            consecutive_milestones = [
                (3, "3日坊主卒業", "3日連続でレシートをアップロードしました"),
                (7, "一週間チャレンジャー", "7日連続でレシートをアップロードしました"),
                (30, "継続は力なり", "30日連続でレシートをアップロードしました")
            ]
            
            for days, name, description in consecutive_milestones:
                if consecutive_days >= days:
                    badge = self._ensure_badge_exists(name, description, {
                        "type": "consecutive_days",
                        "condition": ">=",
                        "value": days
                    })
                    
                    if badge and badge.id not in existing_badges:
                        result = self._award_badge_to_user(user_id, badge.id, badge.name)
                        if result:
                            awarded_badges.append(result)
            
            return awarded_badges
            
        except Exception as e:
            logger.error(f"連続利用バッジ評価エラー: {e}")
            return []
    
    def _evaluate_amount_badges(self, user_id: int, existing_badges: set) -> List[schemas.BadgeAwardResult]:
        """金額系バッジの評価"""
        awarded_badges = []
        
        try:
            # 総購入金額を計算
            user_receipts = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id
            ).all()
            
            total_amount = sum([receipt.total_amount or 0 for receipt in user_receipts])
            
            # 金額バッジを評価
            amount_milestones = [
                (10000, "1万円突破", "累計1万円分のお買い物をしました"),
                (50000, "5万円突破", "累計5万円分のお買い物をしました"),
                (100000, "10万円突破", "累計10万円分のお買い物をしました")
            ]
            
            for amount, name, description in amount_milestones:
                if total_amount >= amount:
                    badge = self._ensure_badge_exists(name, description, {
                        "type": "total_amount",
                        "condition": ">=",
                        "value": amount
                    })
                    
                    if badge and badge.id not in existing_badges:
                        result = self._award_badge_to_user(user_id, badge.id, badge.name)
                        if result:
                            awarded_badges.append(result)
            
            # 高額単発購入バッジの評価
            max_single_purchase = max([receipt.total_amount or 0 for receipt in user_receipts] or [0])
            
            single_purchase_milestones = [
                (5000, "高額お買い物", "一度に5000円以上のお買い物をしました"),
                (10000, "大人買い", "一度に1万円以上のお買い物をしました")
            ]
            
            for amount, name, description in single_purchase_milestones:
                if max_single_purchase >= amount:
                    badge = self._ensure_badge_exists(name, description, {
                        "type": "single_purchase",
                        "condition": ">=",
                        "value": amount
                    })
                    
                    if badge and badge.id not in existing_badges:
                        result = self._award_badge_to_user(user_id, badge.id, badge.name)
                        if result:
                            awarded_badges.append(result)
            
            return awarded_badges
            
        except Exception as e:
            logger.error(f"金額バッジ評価エラー: {e}")
            return []
    
    def _count_consecutive_days(self, receipts: List[models.Receipt]) -> int:
        """連続日数をカウント"""
        if not receipts:
            return 0
        
        # 日付のリストを作成（重複除去）
        upload_dates = list(set([
            receipt.created_at.date() for receipt in receipts
        ]))
        upload_dates.sort(reverse=True)
        
        consecutive_days = 1
        current_date = upload_dates[0]
        
        for i in range(1, len(upload_dates)):
            expected_date = current_date - timedelta(days=i)
            if upload_dates[i] == expected_date:
                consecutive_days += 1
            else:
                break
        
        return consecutive_days
    
    def _ensure_badge_exists(self, name: str, description: str, criteria: Dict[str, Any]) -> Optional[models.Badge]:
        """バッジが存在しない場合は作成する"""
        try:
            # 既存のバッジを確認
            existing_badge = self.db.query(models.Badge).filter(
                models.Badge.name == name
            ).first()
            
            if existing_badge:
                return existing_badge
            
            # 新しいバッジを作成
            new_badge = models.Badge(
                name=name,
                description=description,
                criteria=criteria,
                icon_url=self._get_default_icon_url(criteria.get("type")),
                is_active=True
            )
            
            self.db.add(new_badge)
            self.db.commit()
            self.db.refresh(new_badge)
            
            logger.info(f"新しいバッジを作成: {name}")
            return new_badge
            
        except Exception as e:
            logger.error(f"バッジ作成エラー: {e}")
            self.db.rollback()
            return None
    
    def _get_default_icon_url(self, badge_type: str) -> str:
        """バッジタイプに応じたデフォルトアイコンURLを返す"""
        icon_mapping = {
            "receipt_count": "https://cdn-icons-png.flaticon.com/512/1828/1828506.png",
            "consecutive_days": "https://cdn-icons-png.flaticon.com/512/1827/1827369.png", 
            "total_amount": "https://cdn-icons-png.flaticon.com/512/1827/1827422.png",
            "single_purchase": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
        }
        
        return icon_mapping.get(badge_type, "https://cdn-icons-png.flaticon.com/512/1827/1827380.png")
    
    def _award_badge_to_user(self, user_id: int, badge_id: int, badge_name: str) -> Optional[schemas.BadgeAwardResult]:
        """ユーザーにバッジを授与"""
        try:
            result = crud.award_badge(self.db, user_id, badge_id)
            
            if result:
                logger.info(f"バッジ授与成功: ユーザー{user_id} -> {badge_name}")
                return schemas.BadgeAwardResult(
                    badge_id=badge_id,
                    badge_name=badge_name,
                    is_new=True
                )
            
            return None
            
        except Exception as e:
            logger.error(f"バッジ授与エラー: {e}")
            return None
    
    def create_initial_badges(self) -> bool:
        """初期バッジデータを作成"""
        try:
            initial_badges = [
                # アクティビティバッジ
                {
                    "name": "はじめの一歩",
                    "description": "初回レシートアップロード",
                    "criteria": {"type": "receipt_count", "condition": ">=", "value": 1},
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/1828/1828506.png"
                },
                {
                    "name": "レシート10枚達成",
                    "description": "10枚のレシートをアップロードしました",
                    "criteria": {"type": "receipt_count", "condition": ">=", "value": 10},
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/1828/1828506.png"
                },
                
                # 連続利用バッジ
                {
                    "name": "3日坊主卒業",
                    "description": "3日連続でレシートをアップロードしました",
                    "criteria": {"type": "consecutive_days", "condition": ">=", "value": 3},
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/1827/1827369.png"
                },
                
                # 金額バッジ
                {
                    "name": "1万円突破",
                    "description": "累計1万円分のお買い物をしました",
                    "criteria": {"type": "total_amount", "condition": ">=", "value": 10000},
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/1827/1827422.png"
                }
            ]
            
            for badge_data in initial_badges:
                existing = self.db.query(models.Badge).filter(
                    models.Badge.name == badge_data["name"]
                ).first()
                
                if not existing:
                    badge = models.Badge(**badge_data)
                    self.db.add(badge)
            
            self.db.commit()
            logger.info("初期バッジデータの作成完了")
            return True
            
        except Exception as e:
            logger.error(f"初期バッジデータ作成エラー: {e}")
            self.db.rollback()
            return False