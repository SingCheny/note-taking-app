"""
Supabase REST API client for Vercel deployment
This avoids the need for PostgreSQL drivers in serverless environment
"""
import os
import requests
import json
from datetime import datetime

class SupabaseClient:
    def __init__(self):
        self.url = os.environ.get('SUPABASE_URL')
        self.key = os.environ.get('SUPABASE_KEY')
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def get_notes(self):
        """Get all notes"""
        try:
            response = requests.get(f"{self.url}/rest/v1/notes?order=position.asc", 
                                  headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching notes: {e}")
            return []
    
    def create_note(self, data):
        """Create a new note"""
        try:
            # Ensure we have required fields
            note_data = {
                'title': data.get('title', 'Untitled'),
                'content': data.get('content', ''),
                'tags': data.get('tags', ''),
                'position': data.get('position', 0)
            }
            
            # Add optional fields
            if 'event_date' in data and data['event_date']:
                note_data['event_date'] = data['event_date']
            if 'event_time' in data and data['event_time']:
                note_data['event_time'] = data['event_time']
            
            response = requests.post(f"{self.url}/rest/v1/notes", 
                                   json=note_data, headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                return response.json()[0] if response.json() else note_data
            print(f"Create note error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error creating note: {e}")
            return None
    
    def update_note(self, note_id, data):
        """Update an existing note"""
        try:
            response = requests.patch(f"{self.url}/rest/v1/notes?id=eq.{note_id}", 
                                    json=data, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()[0] if response.json() else data
            print(f"Update note error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error updating note: {e}")
            return None
    
    def delete_note(self, note_id):
        """Delete a note"""
        try:
            response = requests.delete(f"{self.url}/rest/v1/notes?id=eq.{note_id}", 
                                     headers=self.headers, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False