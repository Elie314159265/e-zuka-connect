import re
from typing import List, Tuple
from fastapi import HTTPException, status

class PasswordValidator:
    """
    パスワード強度検証クラス
    """
    
    def __init__(self):
        self.min_length = 8
        self.max_length = 128
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digit = True
        self.require_special = True
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def validate_password(self, password: str) -> Tuple[bool, List[str]]:
        """
        パスワードの強度を検証
        
        Returns:
            Tuple[bool, List[str]]: (有効性, エラーメッセージのリスト)
        """
        errors = []
        
        # 長さチェック
        if len(password) < self.min_length:
            errors.append(f"パスワードは{self.min_length}文字以上である必要があります")
        
        if len(password) > self.max_length:
            errors.append(f"パスワードは{self.max_length}文字以下である必要があります")
        
        # 大文字チェック
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("パスワードには少なくとも1つの大文字を含める必要があります")
        
        # 小文字チェック
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("パスワードには少なくとも1つの小文字を含める必要があります")
        
        # 数字チェック
        if self.require_digit and not re.search(r'[0-9]', password):
            errors.append("パスワードには少なくとも1つの数字を含める必要があります")
        
        # 特殊文字チェック
        if self.require_special and not re.search(f'[{re.escape(self.special_chars)}]', password):
            errors.append(f"パスワードには特殊文字（{self.special_chars}）を少なくとも1つ含める必要があります")
        
        # 一般的なパスワードのブラックリスト
        if self._is_common_password(password):
            errors.append("このパスワードは一般的すぎます。より複雑なパスワードを使用してください")
        
        # 連続する文字のチェック
        if self._has_sequential_chars(password):
            errors.append("パスワードには4文字以上の連続する文字（abcd、1234など）を含めないでください")
        
        # 同じ文字の連続チェック
        if self._has_repeated_chars(password):
            errors.append("パスワードには同じ文字を3回以上連続して使用しないでください")
        
        return len(errors) == 0, errors
    
    def _is_common_password(self, password: str) -> bool:
        """
        一般的なパスワードかどうかをチェック
        """
        common_passwords = [
            "password", "12345678", "qwerty123", "abc123456",
            "password123", "admin123", "welcome123", "test123",
            "user123", "123456789", "qwertyuiop", "asdfghjkl",
            "password1", "123qwe", "admin", "root", "guest"
        ]
        
        return password.lower() in common_passwords
    
    def _has_sequential_chars(self, password: str) -> bool:
        """
        連続する文字があるかチェック（4文字以上の連続のみ禁止）
        """
        password_lower = password.lower()
        
        # アルファベットの連続（4文字以上）
        for i in range(len(password_lower) - 3):
            if (ord(password_lower[i+1]) == ord(password_lower[i]) + 1 and
                ord(password_lower[i+2]) == ord(password_lower[i]) + 2 and
                ord(password_lower[i+3]) == ord(password_lower[i]) + 3):
                return True
        
        # 数字の連続（4文字以上）
        for i in range(len(password) - 3):
            if (password[i:i+4].isdigit() and
                int(password[i+1]) == int(password[i]) + 1 and
                int(password[i+2]) == int(password[i]) + 2 and
                int(password[i+3]) == int(password[i]) + 3):
                return True
        
        return False
    
    def _has_repeated_chars(self, password: str) -> bool:
        """
        同じ文字の連続があるかチェック
        """
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def validate_or_raise(self, password: str):
        """
        パスワードを検証し、無効な場合は例外を発生
        """
        is_valid, errors = self.validate_password(password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "パスワードが強度要件を満たしていません",
                    "errors": errors
                }
            )
    
    def get_strength_score(self, password: str) -> int:
        """
        パスワードの強度スコアを0-100で返す
        """
        score = 0
        
        # 長さによるスコア
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # 文字種によるスコア
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'[0-9]', password):
            score += 10
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            score += 10
        
        # 複雑さによるスコア
        if not self._is_common_password(password):
            score += 10
        if not self._has_sequential_chars(password):
            score += 5
        if not self._has_repeated_chars(password):
            score += 5
        
        return min(score, 100)

# グローバルインスタンス
password_validator = PasswordValidator()