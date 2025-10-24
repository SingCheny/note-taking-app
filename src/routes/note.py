from flask import Blueprint, jsonify, request
from datetime import datetime
from src.models.note import Note, db
from src.llm import translate_to_language, extract_structured_notes
import json

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


@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate the content of a note to a target language using the llm helper."""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json or {}
        target = data.get('target_language')
        if not target:
            return jsonify({'error': 'target_language is required'}), 400

        # Call the llm helper to translate title and content
        translated_title = translate_to_language(note.title or '', target)
        translated_content = translate_to_language(note.content or '', target)

        # Return translated text (do not modify DB automatically)
        return jsonify({
            'translated_title': translated_title,
            'translated_content': translated_content
        }), 200
    except Exception as e:
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


@note_bp.route('/notes/generate', methods=['POST'])
def generate_note():
    """Generate a structured note from user input using LLM extraction."""
    try:
        data = request.json or {}
        user_input = data.get('input', '').strip()
        language = data.get('language', 'English')
        
        if not user_input:
            return jsonify({'error': 'Input text is required'}), 400

        # Call LLM to extract structured notes
        llm_response = extract_structured_notes(user_input, lang=language)
        
        try:
            # Parse the JSON response from LLM
            structured_data = json.loads(llm_response)
            
            # Validate expected fields
            title = structured_data.get('Title', 'Generated Note')
            notes = structured_data.get('Notes', user_input)
            tags = structured_data.get('Tags', [])
            date_str = structured_data.get('Date')
            time_str = structured_data.get('Time')
            
            # Create the note in database
            note = Note(
                title=title,
                content=notes
            )
            
            # Add tags if provided
            if tags and isinstance(tags, list):
                note.tags = ','.join(tags[:3])  # Limit to 3 tags as per system prompt
            
            # Add date if provided and valid
            if date_str:
                try:
                    note.event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass  # Skip invalid dates
            
            # Add time if provided and valid
            if time_str:
                try:
                    note.event_time = datetime.strptime(time_str, '%H:%M').time()
                except (ValueError, TypeError):
                    pass  # Skip invalid times
            
            db.session.add(note)
            db.session.commit()
            
            return jsonify({
                'note': note.to_dict(),
                'structured_data': structured_data
            }), 201
            
        except json.JSONDecodeError:
            # Fallback: create note with original input if LLM didn't return valid JSON
            note = Note(
                title='Generated Note',
                content=llm_response  # Use raw LLM response as content
            )
            
            db.session.add(note)
            db.session.commit()
            
            return jsonify({
                'note': note.to_dict(),
                'warning': 'LLM returned non-JSON response, used as content'
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

