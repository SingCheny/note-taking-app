"""Migration script to move data from SQLite to Supabase PostgreSQL

Usage:
1. Make sure your .env file has the correct DATABASE_URL for Supabase
2. Run: python migrate_data.py
"""

import sqlite3
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def migrate_data():
    # Check if SQLite database exists
    sqlite_path = 'database/app.db'
    if not os.path.exists(sqlite_path):
        print("No SQLite database found to migrate from.")
        return

    # Connect to SQLite
    print("Connecting to SQLite database...")
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables.")
        print("Please set up your .env file with Supabase connection details.")
        return
    
    # Handle postgres:// vs postgresql:// URL schemes
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("Connecting to PostgreSQL database...")
    try:
        pg_conn = psycopg2.connect(database_url)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return

    # Migrate users table (if exists and has data)
    try:
        sqlite_cursor.execute("SELECT * FROM user")
        users = sqlite_cursor.fetchall()
        
        if users:
            print(f"Migrating {len(users)} users...")
            for user in users:
                try:
                    pg_cursor.execute("""
                        INSERT INTO users (id, username, email)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, user)
                except Exception as e:
                    print(f"Error migrating user {user[0]}: {e}")
            
            pg_conn.commit()
            print(f"Successfully migrated {len(users)} users")
    except sqlite3.OperationalError:
        print("No users table found in SQLite database")

    # Migrate notes table
    try:
        sqlite_cursor.execute("SELECT * FROM note ORDER BY id")
        notes = sqlite_cursor.fetchall()
        
        if notes:
            print(f"Migrating {len(notes)} notes...")
            migrated_count = 0
            
            for note in notes:
                try:
                    # SQLite columns: id, title, content, tags, event_date, event_time, position, created_at, updated_at
                    pg_cursor.execute("""
                        INSERT INTO notes (id, title, content, tags, event_date, event_time, position, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, note)
                    migrated_count += 1
                except Exception as e:
                    print(f"Error migrating note {note[0]}: {e}")
            
            pg_conn.commit()
            print(f"Successfully migrated {migrated_count} notes")
        else:
            print("No notes found in SQLite database")
            
    except sqlite3.OperationalError as e:
        print(f"Error reading notes table: {e}")

    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    
    print("\nMigration completed!")
    print("You can now test your app with the Supabase database.")

if __name__ == "__main__":
    migrate_data()