"""
Test script to verify Supabase connection and create tables programmatically
Run this script to test connection and set up database schema
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()

def test_connection_and_setup():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
        
    print("🔄 Testing Supabase connection...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Successfully connected to Supabase!")
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📋 PostgreSQL Version: {version[0]}")
        
        # Create tables
        print("\n🔄 Creating database tables...")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL
            );
        """)
        
        # Create notes table  
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                tags VARCHAR(500),
                event_date DATE,
                event_time TIME,
                position INTEGER DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Create update trigger function
        cursor.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Create trigger
        cursor.execute("""
            DROP TRIGGER IF EXISTS update_notes_updated_at ON notes;
            CREATE TRIGGER update_notes_updated_at 
                BEFORE UPDATE ON notes 
                FOR EACH ROW 
                EXECUTE FUNCTION update_updated_at_column();
        """)
        
        conn.commit()
        print("✅ Database tables created successfully!")
        
        # Verify tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE';
        """)
        
        tables = cursor.fetchall()
        print("\n📊 Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Supabase setup complete! You can now run your Flask app.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Possible solutions:")
        print("1. Check your .env file has the correct DATABASE_URL")
        print("2. Verify your Supabase project is active")
        print("3. Check your database password is correct")
        return False

if __name__ == "__main__":
    success = test_connection_and_setup()
    
    if success:
        print("\n🚀 Next steps:")
        print("1. Run: python src/main.py")
        print("2. Open: http://localhost:5001")
        print("3. Test creating notes in the app")
    else:
        print("\n🔧 Please check your Supabase configuration and try again.")