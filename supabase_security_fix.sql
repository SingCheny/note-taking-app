"""
Supabase 安全修复 - 完整 SQL 脚本
请在 Supabase SQL Editor 中运行此脚本
"""

-- 🔧 Step 1: Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;

-- 🔧 Step 2: Drop existing policies (if any)
DROP POLICY IF EXISTS "Allow all operations on users" ON public.users;
DROP POLICY IF EXISTS "Allow all operations on notes" ON public.notes;

-- 🔧 Step 3: Create comprehensive policies for demo app
CREATE POLICY "Allow all operations on users" ON public.users
FOR ALL 
TO public
USING (true) 
WITH CHECK (true);

CREATE POLICY "Allow all operations on notes" ON public.notes
FOR ALL 
TO public
USING (true) 
WITH CHECK (true);

-- 🔧 Step 4: Grant necessary permissions
GRANT ALL PRIVILEGES ON public.users TO anon, authenticated;
GRANT ALL PRIVILEGES ON public.notes TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE notes_id_seq TO anon, authenticated;

-- 🔧 Step 5: Verify setup
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('users', 'notes');

-- This should return:
-- schemaname | tablename | rowsecurity  
-- public     | users     | t
-- public     | notes     | t