# PostgreSQL Row Level Security (RLS) implementation
# マルチテナンシーのためのデータ分離機能

from sqlalchemy import text
from ..database import engine

def enable_row_level_security():
    """
    PostgreSQL行レベルセキュリティ(RLS)を有効化し、
    マルチテナンシーのためのポリシーを設定する
    """
    
    with engine.connect() as conn:
        # トランザクション開始
        trans = conn.begin()
        
        try:
            # ========== RLS基本設定 ==========
            
            # RLSを有効化（store_idを持つテーブル）
            rls_tables = [
                'events',
                'archive_contents',
                'receipts'  # receiptはstore_idを持つ場合のみ適用
            ]
            
            for table in rls_tables:
                conn.execute(text(f"""
                    ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
                """))
            
            # ========== 店舗用ポリシー ==========
            
            # イベントテーブル：店舗は自分のstore_idのデータのみアクセス可能
            conn.execute(text("""
                DROP POLICY IF EXISTS store_events_policy ON events;
                CREATE POLICY store_events_policy ON events
                FOR ALL
                TO store_role
                USING (store_id = current_setting('app.current_store_id')::int);
            """))
            
            # アーカイブコンテンツテーブル：店舗は自分のstore_idのデータのみアクセス可能
            conn.execute(text("""
                DROP POLICY IF EXISTS store_archive_policy ON archive_contents;
                CREATE POLICY store_archive_policy ON archive_contents
                FOR ALL
                TO store_role
                USING (store_id = current_setting('app.current_store_id')::int);
            """))
            
            # レシートテーブル：店舗は自分のstore_idに関連するレシートのみ閲覧可能
            conn.execute(text("""
                DROP POLICY IF EXISTS store_receipts_policy ON receipts;
                CREATE POLICY store_receipts_policy ON receipts
                FOR SELECT
                TO store_role
                USING (store_id = current_setting('app.current_store_id')::int OR store_id IS NULL);
            """))
            
            # ========== 管理者用ポリシー ==========
            
            # 管理者は全データにアクセス可能
            for table in rls_tables:
                conn.execute(text(f"""
                    DROP POLICY IF EXISTS admin_{table}_policy ON {table};
                    CREATE POLICY admin_{table}_policy ON {table}
                    FOR ALL
                    TO admin_role
                    USING (true);
                """))
            
            # ========== 一般ユーザー用ポリシー ==========
            
            # 一般ユーザーは自分のレシートのみアクセス可能
            conn.execute(text("""
                DROP POLICY IF EXISTS user_receipts_policy ON receipts;
                CREATE POLICY user_receipts_policy ON receipts
                FOR ALL
                TO user_role
                USING (user_id = current_setting('app.current_user_id')::int);
            """))
            
            # イベントは誰でも閲覧可能（SELECT only）
            conn.execute(text("""
                DROP POLICY IF EXISTS public_events_read_policy ON events;
                CREATE POLICY public_events_read_policy ON events
                FOR SELECT
                TO user_role
                USING (is_active = true);
            """))
            
            # アーカイブコンテンツは公開されているもののみ閲覧可能
            conn.execute(text("""
                DROP POLICY IF EXISTS public_archive_read_policy ON archive_contents;
                CREATE POLICY public_archive_read_policy ON archive_contents
                FOR SELECT
                TO user_role
                USING (is_published = true);
            """))
            
            trans.commit()
            print("Row Level Security policies have been successfully applied.")
            
        except Exception as e:
            trans.rollback()
            print(f"Error applying RLS policies: {e}")
            raise

def create_database_roles():
    """
    PostgreSQL データベースロールを作成する
    """
    
    with engine.connect() as conn:
        trans = conn.begin()
        
        try:
            # ロール作成（存在しない場合のみ）
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'admin_role') THEN
                        CREATE ROLE admin_role;
                    END IF;
                    
                    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'store_role') THEN
                        CREATE ROLE store_role;
                    END IF;
                    
                    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user_role') THEN
                        CREATE ROLE user_role;
                    END IF;
                END
                $$;
            """))
            
            # 基本権限の付与
            conn.execute(text("""
                -- 管理者ロール：全テーブルに対する全権限
                GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_role;
                GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_role;
                
                -- 店舗ロール：関連テーブルへの読み書き権限
                GRANT SELECT, INSERT, UPDATE, DELETE ON events, archive_contents TO store_role;
                GRANT SELECT ON receipts, receipt_items, users, weather_data TO store_role;
                GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO store_role;
                
                -- ユーザーロール：限定的な権限
                GRANT SELECT ON events, archive_contents, stores TO user_role;
                GRANT SELECT, INSERT, UPDATE ON receipts, receipt_items TO user_role;
                GRANT SELECT, UPDATE ON users TO user_role;
                GRANT SELECT ON weather_data TO user_role;
                GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO user_role;
            """))
            
            trans.commit()
            print("Database roles have been successfully created.")
            
        except Exception as e:
            trans.rollback()
            print(f"Error creating database roles: {e}")
            raise

def set_session_context(user_id: int = None, store_id: int = None):
    """
    セッションコンテキストを設定する
    RLSポリシーで使用される現在のユーザーID/店舗IDを設定
    """
    
    with engine.connect() as conn:
        if user_id:
            conn.execute(text(f"SET app.current_user_id = {user_id}"))
        if store_id:
            conn.execute(text(f"SET app.current_store_id = {store_id}"))

def reset_session_context():
    """
    セッションコンテキストをリセットする
    """
    
    with engine.connect() as conn:
        conn.execute(text("RESET app.current_user_id"))
        conn.execute(text("RESET app.current_store_id"))

# 初期化関数
def initialize_rls():
    """
    RLS機能を初期化する
    """
    try:
        create_database_roles()
        enable_row_level_security()
        print("RLS initialization completed successfully.")
    except Exception as e:
        print(f"RLS initialization failed: {e}")
        raise