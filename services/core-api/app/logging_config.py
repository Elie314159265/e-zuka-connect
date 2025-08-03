import structlog
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import json

def setup_logging():
    """
    構造化ログを設定
    """
    
    # タイムスタンププロセッサー
    def add_timestamp(logger, method_name, event_dict):
        event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
        return event_dict
    
    # レベルプロセッサー
    def add_level(logger, method_name, event_dict):
        event_dict["level"] = method_name.upper()
        return event_dict
    
    # サービス情報プロセッサー
    def add_service_info(logger, method_name, event_dict):
        event_dict["service"] = "core-api"
        event_dict["version"] = "1.0.0"
        return event_dict
    
    # 構造化ログの設定
    structlog.configure(
        processors=[
            add_timestamp,
            add_level,
            add_service_info,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # 標準ログレベル設定
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

# セキュリティ関連のログ
class SecurityLogger:
    """
    セキュリティ関連のログ専用クラス
    """
    def __init__(self):
        self.logger = structlog.get_logger("security")
    
    def login_attempt(self, email: str, success: bool, ip_address: str = None):
        """ログイン試行ログ"""
        self.logger.info(
            "user_login_attempt",
            email=email,
            success=success,
            ip_address=ip_address,
            event_type="authentication"
        )
    
    def token_refresh(self, email: str, success: bool, ip_address: str = None):
        """トークンリフレッシュログ"""
        self.logger.info(
            "token_refresh",
            email=email,
            success=success,
            ip_address=ip_address,
            event_type="authentication"
        )
    
    def rate_limit_exceeded(self, identifier: str, endpoint: str, limit: str):
        """レート制限違反ログ"""
        self.logger.warning(
            "rate_limit_exceeded",
            identifier=identifier,
            endpoint=endpoint,
            limit=limit,
            event_type="rate_limit"
        )
    
    def unauthorized_access(self, endpoint: str, ip_address: str = None):
        """不正アクセス試行ログ"""
        self.logger.warning(
            "unauthorized_access",
            endpoint=endpoint,
            ip_address=ip_address,
            event_type="security_violation"
        )
    
    def password_change(self, email: str, success: bool):
        """パスワード変更ログ"""
        self.logger.info(
            "password_change",
            email=email,
            success=success,
            event_type="account_security"
        )

# ビジネスロジック関連のログ
class BusinessLogger:
    """
    ビジネスロジック関連のログ専用クラス
    """
    def __init__(self):
        self.logger = structlog.get_logger("business")
    
    def receipt_uploaded(self, user_id: int, receipt_id: int, amount: int):
        """レシートアップロードログ"""
        self.logger.info(
            "receipt_uploaded",
            user_id=user_id,
            receipt_id=receipt_id,
            amount=amount,
            event_type="receipt_processing"
        )
    
    def points_awarded(self, user_id: int, points: int, reason: str):
        """ポイント付与ログ"""
        self.logger.info(
            "points_awarded",
            user_id=user_id,
            points=points,
            reason=reason,
            event_type="gamification"
        )
    
    def badge_earned(self, user_id: int, badge_name: str):
        """バッジ獲得ログ"""
        self.logger.info(
            "badge_earned",
            user_id=user_id,
            badge_name=badge_name,
            event_type="gamification"
        )
    
    def reward_redeemed(self, user_id: int, reward_id: int, points_spent: int):
        """特典交換ログ"""
        self.logger.info(
            "reward_redeemed",
            user_id=user_id,
            reward_id=reward_id,
            points_spent=points_spent,
            event_type="reward_system"
        )

# システム関連のログ
class SystemLogger:
    """
    システム関連のログ専用クラス
    """
    def __init__(self):
        self.logger = structlog.get_logger("system")
    
    def external_api_call(self, service: str, endpoint: str, response_code: int, duration_ms: int):
        """外部API呼び出しログ"""
        self.logger.info(
            "external_api_call",
            service=service,
            endpoint=endpoint,
            response_code=response_code,
            duration_ms=duration_ms,
            event_type="external_integration"
        )
    
    def database_operation(self, operation: str, table: str, duration_ms: int, success: bool):
        """データベース操作ログ"""
        self.logger.info(
            "database_operation",
            operation=operation,
            table=table,
            duration_ms=duration_ms,
            success=success,
            event_type="database"
        )
    
    def error_occurred(self, error_type: str, message: str, trace: str = None):
        """エラー発生ログ"""
        self.logger.error(
            "error_occurred",
            error_type=error_type,
            message=message,
            trace=trace,
            event_type="error"
        )

# グローバルインスタンス
security_logger = SecurityLogger()
business_logger = BusinessLogger()
system_logger = SystemLogger()

# 一般的なログ取得関数
def get_logger(name: str):
    """構造化ログを取得"""
    return structlog.get_logger(name)