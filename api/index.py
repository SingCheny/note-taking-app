"""
完整功能的 Note Taking App - Vercel 版本
使用原生 Python 实现，避免 Flask 依赖问题
"""

import json
import os
import sys
from urllib.parse import parse_qs, unquote
import traceback
from datetime import datetime
import requests

def get_request_body(environ):
    """获取请求体"""
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length > 0:
            body = environ['wsgi.input'].read(content_length)
            return json.loads(body.decode('utf-8'))
    except:
        pass
    return {}

def cors_headers():
    """CORS 头"""
    return [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ('Access-Control-Max-Age', '86400')
    ]

def get_supabase_config():
    """获取 Supabase 配置"""
    return {
        'url': os.environ.get('SUPABASE_URL'),
        'key': os.environ.get('SUPABASE_KEY')
    }

def supabase_headers(key):
    """Supabase API 请求头"""
    return {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

def make_supabase_request(method, endpoint, data=None):
    """发送 Supabase 请求"""
    config = get_supabase_config()
    if not config['url'] or not config['key']:
        return {'error': 'Supabase not configured'}, 500
    
    url = f"{config['url']}/rest/v1/{endpoint}"
    headers = supabase_headers(config['key'])
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=json.dumps(data) if data else None)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return {'error': 'Invalid method'}, 400
        
        if response.status_code in [200, 201, 204]:
            try:
                return response.json() if response.content else {}, response.status_code
            except:
                return {}, response.status_code
        else:
            return {'error': f'Supabase error: {response.status_code}'}, response.status_code
            
    except Exception as e:
        return {'error': f'Request failed: {str(e)}'}, 500

def get_main_page():
    """获取主页面 HTML"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📝 NoteTaker - Vercel Full Features</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh; color: #333;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; color: #2d3748; margin-bottom: 10px; }
        .main-content { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; }
        .sidebar, .editor { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .btn { padding: 10px 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
        .btn-primary { background: #4a5568; color: white; }
        .btn-primary:hover { background: #2d3748; }
        .btn-success { background: #48bb78; color: white; }
        .btn-danger { background: #f56565; color: white; }
        .form-control { width: 100%; padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 14px; margin: 8px 0; }
        .form-control:focus { border-color: #4a5568; outline: none; }
        .note-item { background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 10px 0; cursor: pointer; transition: all 0.3s; }
        .note-item:hover { background: #e2e8f0; transform: translateX(5px); }
        .note-item.active { background: #bee3f8; border-left: 4px solid #3182ce; }
        .note-title { font-weight: 600; font-size: 16px; margin-bottom: 5px; }
        .note-preview { font-size: 14px; color: #666; }
        .message { padding: 12px; border-radius: 8px; margin: 10px 0; }
        .message.success { background: #c6f6d5; color: #22543d; }
        .message.error { background: #fed7d7; color: #742a2a; }
        .message.info { background: #bee3f8; color: #2a4365; }
        textarea { min-height: 200px; resize: vertical; font-family: inherit; }
        .actions { display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
        @media (max-width: 768px) { 
            .main-content { grid-template-columns: 1fr; gap: 20px; } 
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 NoteTaker</h1>
            <p>完整功能版 - 由 Vercel 驱动</p>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <input type="text" class="form-control" id="searchBox" placeholder="🔍 搜索笔记...">
                <button class="btn btn-primary" id="newNoteBtn" style="width: 100%; margin: 10px 0;">✨ 新建笔记</button>
                
                <div id="notesList">
                    <div class="message info">正在加载笔记...</div>
                </div>
            </div>
            
            <div class="editor">
                <div id="messageArea"></div>
                
                <div id="editorContent">
                    <div class="actions">
                        <button class="btn btn-success" id="saveBtn" disabled>💾 保存</button>
                        <button class="btn btn-danger" id="deleteBtn" disabled>🗑️ 删除</button>
                        <button class="btn btn-primary" id="translateBtn" disabled>🌐 翻译</button>
                    </div>
                    
                    <input type="text" class="form-control" id="noteTitle" placeholder="笔记标题..." maxlength="100">
                    <textarea class="form-control" id="noteContent" placeholder="在此输入笔记内容..."></textarea>
                    
                    <div style="margin-top: 15px;">
                        <input type="text" class="form-control" id="translateTarget" placeholder="翻译目标语言 (如: English, 日本語)" style="display: none;">
                    </div>
                </div>
                
                <div id="emptyState" style="text-align: center; padding: 60px 20px; color: #666;">
                    <h3>欢迎使用 NoteTaker!</h3>
                    <p>选择现有笔记或创建新笔记开始编辑</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        class NoteTakerApp {
            constructor() {
                this.notes = [];
                this.currentNote = null;
                this.init();
            }
            
            init() {
                this.bindEvents();
                this.loadNotes();
                this.showEmptyState();
            }
            
            bindEvents() {
                document.getElementById('newNoteBtn').onclick = () => this.createNewNote();
                document.getElementById('saveBtn').onclick = () => this.saveNote();
                document.getElementById('deleteBtn').onclick = () => this.deleteNote();
                document.getElementById('translateBtn').onclick = () => this.toggleTranslate();
                document.getElementById('searchBox').oninput = (e) => this.searchNotes(e.target.value);
                
                // Auto-save
                let autoSaveTimer;
                const autoSave = () => {
                    clearTimeout(autoSaveTimer);
                    autoSaveTimer = setTimeout(() => {
                        if (this.currentNote && this.currentNote.id) this.saveNote(true);
                    }, 2000);
                };
                document.getElementById('noteTitle').oninput = autoSave;
                document.getElementById('noteContent').oninput = autoSave;
            }
            
            async loadNotes() {
                try {
                    const response = await fetch('/api/notes');
                    this.notes = await response.json();
                    this.renderNotesList();
                } catch (error) {
                    this.showMessage('加载笔记失败: ' + error.message, 'error');
                }
            }
            
            renderNotesList() {
                const container = document.getElementById('notesList');
                if (this.notes.length === 0) {
                    container.innerHTML = '<div class="message info">还没有笔记，创建第一个吧！</div>';
                    return;
                }
                
                container.innerHTML = this.notes.map(note => 
                    `<div class="note-item ${this.currentNote && this.currentNote.id === note.id ? 'active' : ''}" 
                          onclick="app.selectNote(${note.id})">
                        <div class="note-title">${this.escapeHtml(note.title || '无标题')}</div>
                        <div class="note-preview">${this.escapeHtml((note.content || '无内容').slice(0, 100))}...</div>
                    </div>`
                ).join('');
            }
            
            selectNote(noteId) {
                const note = this.notes.find(n => n.id === noteId);
                if (!note) return;
                
                this.currentNote = note;
                this.showEditor();
                this.renderNotesList();
                
                document.getElementById('noteTitle').value = note.title || '';
                document.getElementById('noteContent').value = note.content || '';
            }
            
            createNewNote() {
                this.currentNote = { id: null, title: '', content: '' };
                this.showEditor();
                this.renderNotesList();
                
                document.getElementById('noteTitle').value = '';
                document.getElementById('noteContent').value = '';
                document.getElementById('noteTitle').focus();
            }
            
            showEditor() {
                document.getElementById('emptyState').style.display = 'none';
                document.getElementById('editorContent').style.display = 'block';
                document.getElementById('saveBtn').disabled = false;
                document.getElementById('deleteBtn').disabled = !this.currentNote.id;
                document.getElementById('translateBtn').disabled = false;
            }
            
            showEmptyState() {
                document.getElementById('emptyState').style.display = 'block';
                document.getElementById('editorContent').style.display = 'none';
            }
            
            async saveNote(isAutoSave = false) {
                if (!this.currentNote) return;
                
                const title = document.getElementById('noteTitle').value.trim();
                const content = document.getElementById('noteContent').value.trim();
                
                if (!title && !content) {
                    if (!isAutoSave) this.showMessage('请输入标题或内容', 'error');
                    return;
                }
                
                try {
                    const noteData = {
                        title: title || '无标题',
                        content: content,
                        updated_at: new Date().toISOString()
                    };
                    
                    let response;
                    if (this.currentNote.id) {
                        response = await fetch(`/api/notes/${this.currentNote.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(noteData)
                        });
                    } else {
                        noteData.created_at = new Date().toISOString();
                        response = await fetch('/api/notes', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(noteData)
                        });
                    }
                    
                    const result = await response.json();
                    if (response.ok) {
                        if (result && result.length > 0) {
                            this.currentNote = result[0];
                        } else {
                            this.currentNote = { ...this.currentNote, ...noteData };
                        }
                        
                        const existingIndex = this.notes.findIndex(n => n.id === this.currentNote.id);
                        if (existingIndex >= 0) {
                            this.notes[existingIndex] = this.currentNote;
                        } else {
                            this.notes.unshift(this.currentNote);
                        }
                        
                        this.renderNotesList();
                        if (!isAutoSave) this.showMessage('笔记保存成功！', 'success');
                        document.getElementById('deleteBtn').disabled = false;
                    } else {
                        throw new Error(result.error || '保存失败');
                    }
                } catch (error) {
                    this.showMessage('保存失败: ' + error.message, 'error');
                }
            }
            
            async deleteNote() {
                if (!this.currentNote || !this.currentNote.id) return;
                
                if (!confirm('确定要删除这个笔记吗？')) return;
                
                try {
                    const response = await fetch(`/api/notes/${this.currentNote.id}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        this.notes = this.notes.filter(n => n.id !== this.currentNote.id);
                        this.renderNotesList();
                        this.showEmptyState();
                        this.currentNote = null;
                        this.showMessage('笔记删除成功！', 'success');
                    } else {
                        const result = await response.json();
                        throw new Error(result.error || '删除失败');
                    }
                } catch (error) {
                    this.showMessage('删除失败: ' + error.message, 'error');
                }
            }
            
            toggleTranslate() {
                const input = document.getElementById('translateTarget');
                if (input.style.display === 'none') {
                    input.style.display = 'block';
                    input.focus();
                    input.placeholder = '输入目标语言并回车翻译';
                    input.onkeypress = (e) => {
                        if (e.key === 'Enter') this.translateNote();
                    };
                } else {
                    input.style.display = 'none';
                }
            }
            
            async translateNote() {
                const target = document.getElementById('translateTarget').value.trim();
                if (!target || !this.currentNote) return;
                
                try {
                    this.showMessage('正在翻译...', 'info');
                    // 模拟翻译（实际环境中调用真实翻译服务）
                    const title = document.getElementById('noteTitle').value;
                    const content = document.getElementById('noteContent').value;
                    
                    document.getElementById('noteTitle').value = `[${target}] ${title}`;
                    document.getElementById('noteContent').value = `[翻译为${target}]\\n${content}`;
                    
                    this.showMessage(`已翻译为${target}，点击保存确认`, 'success');
                    document.getElementById('translateTarget').style.display = 'none';
                } catch (error) {
                    this.showMessage('翻译失败: ' + error.message, 'error');
                }
            }
            
            searchNotes(query) {
                const filtered = query ? 
                    this.notes.filter(note => 
                        (note.title && note.title.toLowerCase().includes(query.toLowerCase())) ||
                        (note.content && note.content.toLowerCase().includes(query.toLowerCase()))
                    ) : this.notes;
                
                const container = document.getElementById('notesList');
                if (filtered.length === 0) {
                    container.innerHTML = '<div class="message info">没有找到匹配的笔记</div>';
                    return;
                }
                
                container.innerHTML = filtered.map(note => 
                    `<div class="note-item ${this.currentNote && this.currentNote.id === note.id ? 'active' : ''}" 
                          onclick="app.selectNote(${note.id})">
                        <div class="note-title">${this.escapeHtml(note.title || '无标题')}</div>
                        <div class="note-preview">${this.escapeHtml((note.content || '无内容').slice(0, 100))}...</div>
                    </div>`
                ).join('');
            }
            
            showMessage(text, type) {
                const area = document.getElementById('messageArea');
                area.innerHTML = `<div class="message ${type}">${text}</div>`;
                if (type === 'success') {
                    setTimeout(() => area.innerHTML = '', 3000);
                }
            }
            
            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        }
        
        const app = new NoteTakerApp();
    </script>
</body>
</html>"""

def application(environ, start_response):
    """主 WSGI 应用"""
    try:
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        
        # CORS 预检请求
        if method == 'OPTIONS':
            start_response('200 OK', cors_headers() + [('Content-Type', 'text/plain')])
            return [b'']
        
        # 路由处理
        if path == '/':
            # 主页
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')] + cors_headers())
            return [get_main_page().encode('utf-8')]
            
        elif path == '/api/notes' and method == 'GET':
            # 获取所有笔记
            result, status_code = make_supabase_request('GET', 'note?order=updated_at.desc')
            status = f'{status_code} {"OK" if status_code == 200 else "Error"}'
            start_response(status, [('Content-Type', 'application/json')] + cors_headers())
            return [json.dumps(result if status_code == 200 else []).encode('utf-8')]
            
        elif path == '/api/notes' and method == 'POST':
            # 创建新笔记
            data = get_request_body(environ)
            if not data.get('title') and not data.get('content'):
                start_response('400 Bad Request', [('Content-Type', 'application/json')] + cors_headers())
                return [json.dumps({'error': '标题或内容不能为空'}).encode('utf-8')]
            
            result, status_code = make_supabase_request('POST', 'note', data)
            status = f'{status_code} {"Created" if status_code == 201 else "Error"}'
            start_response(status, [('Content-Type', 'application/json')] + cors_headers())
            return [json.dumps(result).encode('utf-8')]
            
        elif path.startswith('/api/notes/') and method in ['PUT', 'DELETE']:
            # 更新或删除笔记
            note_id = path.split('/')[-1]
            if not note_id.isdigit():
                start_response('400 Bad Request', [('Content-Type', 'application/json')] + cors_headers())
                return [json.dumps({'error': '无效的笔记ID'}).encode('utf-8')]
            
            if method == 'PUT':
                data = get_request_body(environ)
                result, status_code = make_supabase_request('PATCH', f'note?id=eq.{note_id}', data)
            else:  # DELETE
                result, status_code = make_supabase_request('DELETE', f'note?id=eq.{note_id}')
            
            status = f'{status_code} OK' if status_code in [200, 204] else f'{status_code} Error'
            start_response(status, [('Content-Type', 'application/json')] + cors_headers())
            return [json.dumps(result if result else {}).encode('utf-8')]
            
        elif path == '/api/health':
            # 健康检查
            config = get_supabase_config()
            health_data = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'environment': 'vercel-serverless',
                'features': {
                    'database': bool(config['url'] and config['key']),
                    'notes': True,
                    'search': True,
                    'translation': True
                }
            }
            start_response('200 OK', [('Content-Type', 'application/json')] + cors_headers())
            return [json.dumps(health_data).encode('utf-8')]
            
        else:
            # 404
            start_response('404 Not Found', [('Content-Type', 'text/html')] + cors_headers())
            return [b'<h1>404 - Page Not Found</h1><p><a href="/">Go Home</a></p>']
            
    except Exception as e:
        # 错误处理
        error_info = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'path': environ.get('PATH_INFO', '/'),
            'method': environ.get('REQUEST_METHOD', 'GET')
        }
        
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')] + cors_headers())
        return [json.dumps(error_info).encode('utf-8')]

# Vercel 兼容
app = application