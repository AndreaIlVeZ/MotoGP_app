"""
Test database connection script
Run this to verify your PostgreSQL connection is working
"""

from app.backend.db import engine
from app.backend.config import settings
from sqlalchemy import text
import sys


def test_connection():
    print("🔍 Testing database connection...")
    print(f"📍 Database URL: {settings.database_url.replace(settings.db_password, '****')}")
    print()
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            
            print("✅ Database connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            print()
            
            # Test creating a simple table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id SERIAL PRIMARY KEY,
                    test_value VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
            
            conn.execute(text("""
                INSERT INTO connection_test (test_value) 
                VALUES ('Connection successful!');
            """))
            conn.commit()
            
            result = conn.execute(text("SELECT * FROM connection_test ORDER BY id DESC LIMIT 1;"))
            row = result.fetchone()
            print(f"✅ Test table created and data inserted!")
            print(f"   Last entry: {row}")
            print()
            
            # Clean up
            conn.execute(text("DROP TABLE connection_test;"))
            conn.commit()
            print("🧹 Test table cleaned up")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"   Error: {str(e)}")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check your DATABASE_URL in .env file")
        print("   3. Verify the database exists: createdb motogp_db")
        print("   4. Check credentials (username/password)")
        print()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
