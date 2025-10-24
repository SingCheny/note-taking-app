"""
Alternative Supabase setup using REST API
This script uses Supabase REST API instead of direct PostgreSQL connection
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def setup_supabase_via_api():
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase URL or Key not found in .env file")
        return False
    
    print("🔄 Testing Supabase REST API connection...")
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test connection by checking if we can access the API
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully connected to Supabase REST API!")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        # Check if tables exist
        notes_response = requests.get(f"{supabase_url}/rest/v1/notes?limit=1", headers=headers)
        users_response = requests.get(f"{supabase_url}/rest/v1/users?limit=1", headers=headers)
        
        if notes_response.status_code == 200 and users_response.status_code == 200:
            print("✅ Database tables already exist and are accessible!")
            return True
        else:
            print("📋 Tables may not exist yet. You'll need to create them manually.")
            print("\n📝 SQL to run in Supabase SQL Editor:")
            print("""
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

-- Create notes table  
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

-- Create update trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger
DROP TRIGGER IF EXISTS update_notes_updated_at ON notes;
CREATE TRIGGER update_notes_updated_at 
    BEFORE UPDATE ON notes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
            """)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Connection timeout. Please check your internet connection.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Supabase REST API Setup")
    print("=" * 40)
    
    success = setup_supabase_via_api()
    
    if success:
        print("\n🎉 Supabase is ready!")
        print("\n🚀 Next steps:")
        print("1. Run: python src/main.py")
        print("2. Open: http://localhost:5001")
        print("3. Test creating notes in the app")
    else:
        print("\n📋 Manual Setup Required:")
        print("1. Go to: https://supabase.com/dashboard")
        print("2. Select your project: ujunndegjyuycbjtrutf")
        print("3. Go to SQL Editor")
        print("4. Run the SQL code shown above")
        print("5. Then try running: python src/main.py")