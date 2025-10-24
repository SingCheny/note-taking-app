"""
Export functionality for notes
"""
from flask import jsonify, request
import json
import csv
from io import StringIO
from datetime import datetime

def export_notes_json(notes):
    """Export notes as JSON"""
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'total_notes': len(notes),
        'notes': [note.to_dict() for note in notes]
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def export_notes_csv(notes):
    """Export notes as CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Title', 'Content', 'Tags', 'Event Date', 'Event Time', 'Position', 'Created At', 'Updated At'])
    
    # Write data
    for note in notes:
        writer.writerow([
            note.id,
            note.title,
            note.content,
            note.tags or '',
            note.event_date or '',
            note.event_time or '',
            note.position,
            note.created_at,
            note.updated_at
        ])
    
    return output.getvalue()

def export_notes_markdown(notes):
    """Export notes as Markdown"""
    md_content = f"# Notes Export\n\n"
    md_content += f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for note in notes:
        md_content += f"## {note.title}\n\n"
        md_content += f"{note.content}\n\n"
        
        if note.tags:
            md_content += f"**Tags:** {note.tags}\n\n"
        
        if note.event_date or note.event_time:
            md_content += f"**Event:** {note.event_date or ''} {note.event_time or ''}\n\n"
        
        md_content += "---\n\n"
    
    return md_content