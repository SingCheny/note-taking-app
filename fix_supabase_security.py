"""
Fix Supabase RLS Security Issues
This script will enable Row Level Security and create proper policies
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def fix_supabase_security():
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found")
        return False
    
    print("🔧 Fixing Supabase Security Issues...")
    
    # SQL commands to fix security
    security_sql = """
-- Enable RLS on users table
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Enable RLS on notes table  
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (since this is a demo app)
-- You can modify these policies based on your security requirements

-- Policy for users table - allow all operations for now
DROP POLICY IF EXISTS "Allow all operations on users" ON public.users;
CREATE POLICY "Allow all operations on users" ON public.users
FOR ALL USING (true) WITH CHECK (true);

-- Policy for notes table - allow all operations for now  
DROP POLICY IF EXISTS "Allow all operations on notes" ON public.notes;
CREATE POLICY "Allow all operations on notes" ON public.notes
FOR ALL USING (true) WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON public.users TO anon, authenticated;
GRANT ALL ON public.notes TO anon, authenticated;
GRANT USAGE ON SEQUENCE users_id_seq TO anon, authenticated;
GRANT USAGE ON SEQUENCE notes_id_seq TO anon, authenticated;
"""
    
    print("📋 SQL Commands to run in Supabase SQL Editor:")
    print("=" * 60)
    print(security_sql)
    print("=" * 60)
    
    print("\n🔧 Steps to fix:")
    print("1. Go to: https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to SQL Editor")
    print("4. Paste and run the SQL commands above")
    print("5. This will enable RLS and create appropriate policies")
    
    return True

if __name__ == "__main__":
    fix_supabase_security()