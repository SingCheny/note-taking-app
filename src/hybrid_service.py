"""
Hybrid data service that can use either SQLAlchemy or Supabase REST API
"""
import os
from typing import List, Dict, Optional

def get_data_service():
    """Get appropriate data service based on environment"""
    if os.environ.get('VERCEL_ENV') and os.environ.get('SUPABASE_URL'):
        # In Vercel with Supabase credentials, use REST API
        from .supabase_client import SupabaseClient
        return SupabaseClient()
    else:
        # Use SQLAlchemy (local or direct PostgreSQL)
        return None  # Will use normal SQLAlchemy routes

class HybridDataService:
    def __init__(self):
        self.use_supabase = bool(os.environ.get('VERCEL_ENV') and os.environ.get('SUPABASE_URL'))
        if self.use_supabase:
            from .supabase_client import SupabaseClient
            self.supabase = SupabaseClient()
    
    def get_notes(self):
        if self.use_supabase:
            return self.supabase.get_notes()
        else:
            # Use SQLAlchemy
            from .models.note import Note
            notes = Note.query.order_by(Note.position).all()
            return [note.to_dict() for note in notes]
    
    def create_note(self, data):
        if self.use_supabase:
            return self.supabase.create_note(data)
        else:
            # Use SQLAlchemy
            from .models.note import Note
            from .models.user import db
            note = Note(
                title=data.get('title', 'Untitled'),
                content=data.get('content', ''),
                tags=data.get('tags', ''),
                position=data.get('position', 0),
                event_date=data.get('event_date'),
                event_time=data.get('event_time')
            )
            db.session.add(note)
            db.session.commit()
            return note.to_dict()
    
    def update_note(self, note_id, data):
        if self.use_supabase:
            return self.supabase.update_note(note_id, data)
        else:
            # Use SQLAlchemy
            from .models.note import Note
            from .models.user import db
            note = Note.query.get(note_id)
            if note:
                for key, value in data.items():
                    if hasattr(note, key):
                        setattr(note, key, value)
                db.session.commit()
                return note.to_dict()
            return None
    
    def delete_note(self, note_id):
        if self.use_supabase:
            return self.supabase.delete_note(note_id)
        else:
            # Use SQLAlchemy
            from .models.note import Note
            from .models.user import db
            note = Note.query.get(note_id)
            if note:
                db.session.delete(note)
                db.session.commit()
                return True
            return False