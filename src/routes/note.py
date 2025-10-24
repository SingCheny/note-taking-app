from flask import Blueprint, jsonify, request
from datetime import datetime
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    # Order by position (ascending) when available, then by most recently updated
    notes = Note.query.order_by(Note.position.asc(), Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Initialize note with required fields
        note = Note(title=data['title'], content=data['content'])
        
        # Handle optional fields
        if 'tags' in data and isinstance(data['tags'], list):
            note.tags = ','.join(data['tags'])
        
        if 'event_date' in data and data['event_date']:
            note.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            
        if 'event_time' in data and data['event_time']:
            # accept HH:MM or HH:MM:SS formats from client
            et = data['event_time']
            parsed = None
            for fmt in ('%H:%M', '%H:%M:%S'):
                try:
                    parsed = datetime.strptime(et, fmt).time()
                    break
                except Exception:
                    parsed = None
            if parsed is None:
                return jsonify({'error': 'Invalid event_time format'}), 400
            note.event_time = parsed
        
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update basic fields
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        
        # Update tags if provided
        if 'tags' in data:
            if isinstance(data['tags'], list):
                note.tags = ','.join(data['tags'])
            else:
                note.tags = None
                
        # Update event date if provided
        if 'event_date' in data:
            if data['event_date']:
                note.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            else:
                note.event_date = None
                
        # Update event time if provided (accept HH:MM or HH:MM:SS)
        if 'event_time' in data:
            if data['event_time']:
                et = data['event_time']
                parsed = None
                for fmt in ('%H:%M', '%H:%M:%S'):
                    try:
                        parsed = datetime.strptime(et, fmt).time()
                        break
                    except Exception:
                        parsed = None
                if parsed is None:
                    return jsonify({'error': 'Invalid event_time format'}), 400
                note.event_time = parsed
            else:
                note.event_time = None
        
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])


@note_bp.route('/notes/reorder', methods=['POST'])
def reorder_notes():
    """Reorder notes. Expects JSON: { "order": [<note_id>, ...] }"""
    try:
        data = request.json
        if not data or 'order' not in data or not isinstance(data['order'], list):
            return jsonify({'error': 'Order list required'}), 400

        for idx, note_id in enumerate(data['order']):
            note = Note.query.get(note_id)
            if note:
                note.position = idx

        db.session.commit()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

