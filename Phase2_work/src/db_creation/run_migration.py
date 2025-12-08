"""
Migration Script: Add submission_status column to Applications table
Date: 8 December 2025
"""
import mysql.connector
import os
from pathlib import Path

# Try to load .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

# Get database credentials from environment or defaults
HOST = os.getenv('HOST', 'localhost')
MYSQL_USER = os.getenv('GG_USER', 'root')
MYSQL_PASS = os.getenv('GG_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'GrantGuruDB')

def run_migration():
    """Run the database migration to add submission_status column"""
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()

        print(f"Connected to database: {DB_NAME}")

        # Check if column already exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = 'Applications'
            AND COLUMN_NAME = 'submission_status'
        """, (DB_NAME,))

        column_exists = cursor.fetchone()[0] > 0

        if column_exists:
            print("[OK] Column 'submission_status' already exists. No migration needed.")
            return True

        print("Adding 'submission_status' column to Applications table...")

        # Add the column
        cursor.execute("""
            ALTER TABLE Applications
            ADD COLUMN submission_status ENUM('started', 'submitted') NOT NULL DEFAULT 'started'
            AFTER grant_id
        """)

        print("[OK] Column 'submission_status' added successfully")

        # Check if index exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = 'Applications'
            AND INDEX_NAME = 'idx_application_submission_status'
        """, (DB_NAME,))

        index_exists = cursor.fetchone()[0] > 0

        if not index_exists:
            print("Creating index on 'submission_status' column...")
            cursor.execute("""
                CREATE INDEX idx_application_submission_status ON Applications(submission_status)
            """)
            print("[OK] Index created successfully")
        else:
            print("[OK] Index already exists")

        conn.commit()
        print("\n[OK] Migration completed successfully!")
        return True

    except mysql.connector.Error as e:
        print(f"[ERROR] Database error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    print("=" * 50)
    print("Running Database Migration")
    print("=" * 50)
    success = run_migration()
    print("=" * 50)
    exit(0 if success else 1)
