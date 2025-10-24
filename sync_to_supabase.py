#!/usr/bin/env python3
"""
数据同步工具：将本地 SQLite 数据同步到 Supabase
"""

import sqlite3
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_supabase_config():
    """获取 Supabase 配置"""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        raise ValueError("❌ 请确保 .env 文件中有 SUPABASE_URL 和 SUPABASE_KEY")
    
    return url, key

def get_local_notes():
    """从本地 SQLite 获取所有笔记"""
    db_path = 'database/app.db'
    if not os.path.exists(db_path):
        print("❌ 本地数据库不存在")
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, title, content, created_at, updated_at
            FROM note
            ORDER BY created_at
        """)
        notes = cursor.fetchall()
        print(f"📖 本地找到 {len(notes)} 条笔记")
        return notes
    except Exception as e:
        print(f"❌ 读取本地数据失败: {e}")
        return []
    finally:
        conn.close()

def sync_notes_to_supabase(notes):
    """同步笔记到 Supabase"""
    if not notes:
        print("📝 没有笔记需要同步")
        return
    
    url, key = get_supabase_config()
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    # 首先检查 Supabase 中的现有数据
    print("🔍 检查 Supabase 中的现有笔记...")
    response = requests.get(f'{url}/rest/v1/notes', headers=headers)
    
    existing_notes = []
    if response.status_code == 200:
        existing_notes = response.json()
        print(f"🔄 Supabase 中已有 {len(existing_notes)} 条笔记")
    
    # 创建现有笔记ID集合
    existing_ids = {note['id'] for note in existing_notes}
    
    # 同步新笔记
    success_count = 0
    error_count = 0
    
    for note in notes:
        note_id, title, content, created_at, updated_at = note
        
        # 跳过已存在的笔记
        if note_id in existing_ids:
            print(f"⏭️  跳过已存在的笔记 ID: {note_id}")
            continue
        
        note_data = {
            'id': note_id,
            'title': title,
            'content': content,
            'created_at': created_at,
            'updated_at': updated_at
        }
        
        try:
            response = requests.post(
                f'{url}/rest/v1/notes',
                headers=headers,
                data=json.dumps(note_data)
            )
            
            if response.status_code == 201:
                print(f"✅ 成功同步笔记: {title[:30]}...")
                success_count += 1
            else:
                print(f"❌ 同步失败 {title[:30]}...: {response.status_code} - {response.text}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ 同步出错 {title[:30]}...: {e}")
            error_count += 1
    
    print(f"\n📊 同步完成:")
    print(f"   ✅ 成功: {success_count} 条")
    print(f"   ❌ 失败: {error_count} 条")
    print(f"   ⏭️  跳过: {len(notes) - success_count - error_count} 条")

def check_supabase_data():
    """检查 Supabase 中的数据"""
    url, key = get_supabase_config()
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 检查 Supabase 数据...")
    response = requests.get(f'{url}/rest/v1/notes?order=created_at.desc', headers=headers)
    
    if response.status_code == 200:
        notes = response.json()
        print(f"📊 Supabase 中共有 {len(notes)} 条笔记")
        
        if notes:
            print("📋 最新的笔记:")
            for i, note in enumerate(notes[:3]):
                content_preview = note['content'][:50] + "..." if len(note['content']) > 50 else note['content']
                print(f"   {i+1}. {note['title']} | {content_preview}")
    else:
        print(f"❌ 获取 Supabase 数据失败: {response.status_code}")

def main():
    print("🚀 数据同步工具")
    print("=" * 50)
    
    try:
        # 1. 检查配置
        get_supabase_config()
        print("✅ Supabase 配置正常")
        
        # 2. 获取本地数据
        local_notes = get_local_notes()
        
        # 3. 同步到 Supabase
        if local_notes:
            sync_notes_to_supabase(local_notes)
        
        # 4. 检查同步结果
        print("\n" + "=" * 50)
        check_supabase_data()
        
    except Exception as e:
        print(f"❌ 同步过程出错: {e}")

if __name__ == "__main__":
    main()