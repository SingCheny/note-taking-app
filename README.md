# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

##  Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

##  Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

##  Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **SQLite**: Lightweight, file-based database for data persistence

##  Project Structure

\\\
notetaking-app/
 src/
    models/
       user.py          # User model (template)
       note.py          # Note model with database schema
    routes/
       user.py          # User API routes (template)
       note.py          # Note API endpoints
    static/
       index.html       # Frontend application
    database/
       app.db           # SQLite database file
    main.py              # Flask application entry point
 api/
    index.py             # Vercel serverless entry point
 venv/                    # Python virtual environment
 requirements.txt         # Python dependencies
 vercel.json              # Vercel configuration
 README.md               # This file
\\\

##  Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   \\\ash
   git clone https://github.com/SingCheny/note-taking-app.git
   cd note-taking-app
   \\\

2. **Create virtual environment**
   \\\ash
   python -m venv venv
   \\\

3. **Activate the virtual environment**
   \\\ash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   \\\

4. **Install dependencies**
   \\\ash
   pip install -r requirements.txt
   \\\

5. **Run the application**
   \\\ash
   python src/main.py
   \\\

6. **Access the application**
   - Open your browser and go to \http://localhost:5001\

##  API Endpoints

### Notes API
- \GET /api/notes\ - Get all notes
- \POST /api/notes\ - Create a new note
- \GET /api/notes/<id>\ - Get a specific note
- \PUT /api/notes/<id>\ - Update a note
- \DELETE /api/notes/<id>\ - Delete a note
- \GET /api/notes/search?q=<query>\ - Search notes
- \POST /api/notes/<id>/translate\ - Translate note to target language
- \POST /api/notes/generate\ - Generate note from text using LLM
- \GET /api/health\ - Health check endpoint

### Request/Response Format
\\\json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321",
  "tags": ["work", "important"],
  "event_date": "2025-10-25",
  "event_time": "17:00"
}
\\\

##  User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Translate Button**: Translate notes to different languages
- **Generate Notes**: Create structured notes from natural language
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack
- **Theme Switcher**: Toggle between default and warm themes

##  Database Schema

### Notes Table
\\\sql
CREATE TABLE note (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags VARCHAR(200),
    event_date DATE,
    event_time TIME,
    position INTEGER
);
\\\

##  Deployment

### Vercel Deployment

1. **Push code to GitHub**
   \\\ash
   git push origin main
   \\\

2. **Import project in Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Configure environment variables

3. **Set Environment Variables in Vercel**
   - \GITHUB_TOKEN\ - Your GitHub personal access token
   - \SECRET_KEY\ - Flask secret key
   - \VERCEL_ENV\ - Set automatically by Vercel

4. **Deploy**
   - Vercel will automatically deploy on every push to main

### Environment Variables
- \FLASK_ENV\: Set to \development\ for debug mode
- \SECRET_KEY\: Flask secret key for sessions
- \GITHUB_TOKEN\: GitHub token for LLM API access
- \VERCEL_ENV\: Automatically set by Vercel platform

### Database Configuration
- **Local**: File-based SQLite (\src/database/app.db\)
- **Vercel**: In-memory SQLite (serverless environment)
- Automatic table creation on first run
- SQLAlchemy ORM for database operations

##  AI Features

### LLM Integration
- **Translation**: Translate note titles and content to different languages
- **Note Generation**: Extract structured notes from natural language input
- **Date/Time Extraction**: Automatically parse dates and times from text

### Supported Languages
- English
- Chinese (Simplified & Traditional)
- Spanish
- French
- German
- Japanese
- And more...

##  Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

##  Configuration Files

- \equirements.txt\ - Python dependencies
- \ercel.json\ - Vercel deployment configuration
- \pi/index.py\ - Vercel serverless entry point
- \.env\ - Local environment variables (not committed)

##  License

This project is open source and available under the MIT License.

##  Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version
5. Verify environment variables are set correctly

##  Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Persistent database with Supabase/PostgreSQL
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities
- Voice-to-text note creation
- Advanced search with filters

---

**Built with  using Flask, SQLite, and modern web technologies**

*Last updated: October 25, 2025*
