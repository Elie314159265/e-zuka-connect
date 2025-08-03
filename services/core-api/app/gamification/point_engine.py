"""
ポイント計算エンジン
レシートアップロード時のポイント自動付与システム
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models, schemas
import logging

logger = logging.getLogger(__name__)

class PointCalculationEngine:
    """
    ポイント計算エンジン
    レシートデータ、ユーザープロファイル、アップロードコンテキストを基に
    適切なポイントを計算する
    """
    
    def __init__(self, db: Session):
        self.db = db
        
    def calculate_points(
        self, 
        receipt_data: Dict[str, Any], 
        user_id: int,
        upload_context: Dict[str, Any] = None
    ) -> schemas.PointCalculationResult:
        """
        ポイント計算のメイン処理
        
        Args:
            receipt_data: レシート情報（金額、店舗、商品など）
            user_id: ユーザーID
            upload_context: アップロード状況（時刻、天候など）
            
        Returns:
            PointCalculationResult: 計算結果
        """
        try:
            base_points = self._calculate_base_points(receipt_data)
            bonus_details = []
            total_bonus = 0
            
            # 各種ボーナス計算
            amount_bonus, amount_detail = self._calculate_amount_bonus(receipt_data)
            if amount_bonus > 0:
                bonus_details.append(amount_detail)
                total_bonus += amount_bonus
            
            consecutive_bonus, consecutive_detail = self._calculate_consecutive_bonus(user_id)
            if consecutive_bonus > 0:
                bonus_details.append(consecutive_detail)
                total_bonus += consecutive_bonus
            
            first_time_bonus, first_time_detail = self._calculate_first_time_bonus(user_id)
            if first_time_bonus > 0:
                bonus_details.append(first_time_detail)
                total_bonus += first_time_bonus
            
            if upload_context:
                weather_bonus, weather_detail = self._calculate_weather_bonus(upload_context)
                if weather_bonus > 0:
                    bonus_details.append(weather_detail)
                    total_bonus += weather_bonus
                
                time_bonus, time_detail = self._calculate_time_bonus(upload_context)
                if time_bonus > 0:
                    bonus_details.append(time_detail)
                    total_bonus += time_bonus
            
            store_bonus, store_detail = self._calculate_store_bonus(receipt_data)
            if store_bonus > 0:
                bonus_details.append(store_detail)
                total_bonus += store_bonus
            
            total_points = base_points + total_bonus
            
            return schemas.PointCalculationResult(
                base_points=base_points,
                bonus_points=total_bonus,
                total_points=total_points,
                bonus_details=bonus_details
            )
            
        except Exception as e:
            logger.error(f"ポイント計算エラー: {e}")
            # エラー時は基本ポイントのみ返す
            return schemas.PointCalculationResult(
                base_points=10,
                bonus_points=0,
                total_points=10,
                bonus_details=[{"type": "error", "message": "ボーナス計算エラー"}]
            )
    
    def _calculate_base_points(self, receipt_data: Dict[str, Any]) -> int:
        """基本ポイント計算"""
        # OCR解析が成功していることが前提
        if not receipt_data.get("supplier_name") or not receipt_data.get("total_amount"):
            return 5  # 不完全なデータの場合は減額
        
        return 10  # 基本ポイント
    
    def _calculate_amount_bonus(self, receipt_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """購入金額ボーナス計算"""
        total_amount = receipt_data.get("total_amount", 0)
        
        if total_amount >= 3000:
            return 50, {
                "type": "amount_bonus",
                "name": "高額購入ボーナス",
                "points": 50,
                "condition": "3000円以上",
                "amount": total_amount
            }
        elif total_amount >= 1000:
            return 20, {
                "type": "amount_bonus", 
                "name": "まとめ買いボーナス",
                "points": 20,
                "condition": "1000円以上",
                "amount": total_amount
            }
        elif total_amount >= 500:
            return 10, {
                "type": "amount_bonus",
                "name": "お買い物ボーナス",
                "points": 10,
                "condition": "500円以上",
                "amount": total_amount
            }
        elif total_amount >= 100:
            return 5, {
                "type": "amount_bonus",
                "name": "ちょこっと買いボーナス",
                "points": 5,
                "condition": "100円以上",
                "amount": total_amount
            }
        
        return 0, {}
    
    def _calculate_consecutive_bonus(self, user_id: int) -> Tuple[int, Dict[str, Any]]:
        """連続利用ボーナス計算"""
        try:
            # 過去30日間のレシートアップロード履歴を取得
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_receipts = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id,
                models.Receipt.created_at >= thirty_days_ago
            ).order_by(models.Receipt.created_at.desc()).all()
            
            if not recent_receipts:
                return 0, {}
            
            # 連続日数を計算
            consecutive_days = self._count_consecutive_days(recent_receipts)
            
            if consecutive_days >= 30:
                return 100, {
                    "type": "consecutive_bonus",
                    "name": "継続は力なり（30日連続）",
                    "points": 100,
                    "consecutive_days": consecutive_days
                }
            elif consecutive_days >= 7:
                return 50, {
                    "type": "consecutive_bonus",
                    "name": "一週間チャレンジャー",
                    "points": 50,
                    "consecutive_days": consecutive_days
                }
            elif consecutive_days >= 3:
                return 20, {
                    "type": "consecutive_bonus",
                    "name": "3日坊主卒業",
                    "points": 20,
                    "consecutive_days": consecutive_days
                }
            
            return 0, {}
            
        except Exception as e:
            logger.error(f"連続利用ボーナス計算エラー: {e}")
            return 0, {}
    
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
    
    def _calculate_first_time_bonus(self, user_id: int) -> Tuple[int, Dict[str, Any]]:
        """初回ボーナス計算"""
        try:
            # ユーザーのレシート総数を確認
            receipt_count = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id
            ).count()
            
            if receipt_count == 1:  # 初回アップロード
                return 50, {
                    "type": "first_time_bonus",
                    "name": "初回アップロードボーナス",
                    "points": 50,
                    "message": "初めてのレシートアップロードありがとうございます！"
                }
            
            return 0, {}
            
        except Exception as e:
            logger.error(f"初回ボーナス計算エラー: {e}")
            return 0, {}
    
    def _calculate_weather_bonus(self, upload_context: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """天候ボーナス計算"""
        weather_code = upload_context.get("weather_code")
        
        if not weather_code:
            return 0, {}
        
        # WMO Weather interpretation codes
        # 雪系: 71-77, 85-86
        if weather_code in [71, 73, 75, 77, 85, 86]:
            return 25, {
                "type": "weather_bonus",
                "name": "雪の日お疲れさまボーナス",
                "points": 25,
                "weather_code": weather_code
            }
        
        # 雨系: 51-67, 80-82
        elif weather_code in range(51, 68) or weather_code in [80, 81, 82]:
            return 15, {
                "type": "weather_bonus", 
                "name": "雨の日お疲れさまボーナス",
                "points": 15,
                "weather_code": weather_code
            }
        
        return 0, {}
    
    def _calculate_time_bonus(self, upload_context: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """時間帯ボーナス計算"""
        upload_time = upload_context.get("upload_time")
        
        if not upload_time:
            return 0, {}
        
        hour = upload_time.hour
        
        # 早朝ボーナス (6-9時)
        if 6 <= hour < 9:
            return 10, {
                "type": "time_bonus",
                "name": "早起きボーナス",
                "points": 10,
                "hour": hour
            }
        
        # 夜間ボーナス (18-21時)
        elif 18 <= hour < 21:
            return 5, {
                "type": "time_bonus",
                "name": "お疲れさまボーナス", 
                "points": 5,
                "hour": hour
            }
        
        # 土日祝日ボーナス
        if upload_time.weekday() >= 5:  # 土日
            return 5, {
                "type": "time_bonus",
                "name": "週末ボーナス",
                "points": 5,
                "weekday": upload_time.weekday()
            }
        
        return 0, {}
    
    def _calculate_store_bonus(self, receipt_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """店舗連携ボーナス計算"""
        store_id = receipt_data.get("store_id")
        supplier_name = receipt_data.get("supplier_name", "")
        
        # データベースの店舗情報と照合
        if store_id:
            try:
                store = self.db.query(models.Store).filter(
                    models.Store.id == store_id
                ).first()
                
                if store:
                    # 商店街加盟店ボーナス
                    return 10, {
                        "type": "store_bonus",
                        "name": "商店街加盟店ボーナス",
                        "points": 10,
                        "store_name": store.name
                    }
            except Exception as e:
                logger.error(f"店舗ボーナス計算エラー: {e}")
        
        # 店舗名から推定（簡易版）
        individual_keywords = ["商店", "個人", "家族", "〜屋", "〜店"]
        for keyword in individual_keywords:
            if keyword in supplier_name:
                return 15, {
                    "type": "store_bonus",
                    "name": "個人商店応援ボーナス",
                    "points": 15,
                    "store_name": supplier_name
                }
        
        return 0, {}
    
    def is_duplicate_receipt(
        self, 
        receipt_data: Dict[str, Any], 
        user_id: int
    ) -> bool:
        """
        重複レシート判定
        同一店舗、同一金額、同一日時（±30分）の重複をチェック
        """
        try:
            supplier_name = receipt_data.get("supplier_name")
            total_amount = receipt_data.get("total_amount")
            receipt_date = receipt_data.get("receipt_date")
            
            if not all([supplier_name, total_amount, receipt_date]):
                return False
            
            # ±30分の範囲で重複チェック
            time_margin = timedelta(minutes=30)
            start_time = receipt_date - time_margin
            end_time = receipt_date + time_margin
            
            existing_receipt = self.db.query(models.Receipt).filter(
                models.Receipt.user_id == user_id,
                models.Receipt.supplier_name == supplier_name,
                models.Receipt.total_amount == total_amount,
                models.Receipt.receipt_date >= start_time,
                models.Receipt.receipt_date <= end_time
            ).first()
            
            return existing_receipt is not None
            
        except Exception as e:
            logger.error(f"重複チェックエラー: {e}")
            return False