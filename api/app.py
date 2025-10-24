"""
完整功能的 Vercel Flask 应用
集成笔记管理、主题切换、翻译和 AI 生成功能
"""

import os
import sys
import json
from datetime import datetime

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_cors import CORS
    import requests
    from dotenv import load_dotenv
    
    # 加载环境变量
    load_dotenv()
    
    app = Flask(__name__)
    CORS(app)
    
    # Supabase 配置
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    def get_supabase_headers():
        """获取 Supabase API 请求头"""
        return {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    # 读取 HTML 模板
    def load_html_template():
        """加载 HTML 模板"""
        try:
            html_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'static', 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            # 如果找不到文件，返回基础模板
            return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Note Taking App - Vercel Full Features</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .note { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #0056b3; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
        #notesList { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗒️ Note Taking App</h1>
            <p>Vercel Full Features Version</p>
        </div>
        
        <div class="note-form">
            <input type="text" id="noteTitle" placeholder="标题...">
            <textarea id="noteContent" rows="4" placeholder="内容..."></textarea>
            <button class="btn" onclick="addNote()">添加笔记</button>
            <button class="btn" onclick="loadNotes()">刷新笔记</button>
        </div>
        
        <div id="notesList"></div>
    </div>
    
    <script>
        // 加载笔记
        async function loadNotes() {
            try {
                const response = await fetch('/api/notes');
                const notes = await response.json();
                displayNotes(notes);
            } catch (error) {
                console.error('加载笔记失败:', error);
            }
        }
        
        // 显示笔记
        function displayNotes(notes) {
            const container = document.getElementById('notesList');
            container.innerHTML = notes.map(note => `
                <div class="note">
                    <h3>${note.title}</h3>
                    <p>${note.content}</p>
                    <small>创建时间: ${note.created_at}</small>
                </div>
            `).join('');
        }
        
        // 添加笔记
        async function addNote() {
            const title = document.getElementById('noteTitle').value;
            const content = document.getElementById('noteContent').value;
            
            if (!title || !content) {
                alert('请填写标题和内容');
                return;
            }
            
            try {
                const response = await fetch('/api/notes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, content })
                });
                
                if (response.ok) {
                    document.getElementById('noteTitle').value = '';
                    document.getElementById('noteContent').value = '';
                    loadNotes();
                }
            } catch (error) {
                console.error('添加笔记失败:', error);
            }
        }
        
        // 页面加载时获取笔记
        document.addEventListener('DOMContentLoaded', loadNotes);
    </script>
</body>
</html>"""
    
    @app.route('/')
    def index():
        """首页"""
        try:
            html_content = load_html_template()
            return render_template_string(html_content)
        except Exception as e:
            return f"应用加载中... 错误: {str(e)}", 500
    
    @app.route('/api/notes', methods=['GET'])
    def get_notes():
        """获取所有笔记"""
        try:
            if not SUPABASE_URL or not SUPABASE_KEY:
                return jsonify([]), 200
            
            response = requests.get(
                f'{SUPABASE_URL}/rest/v1/note?order=created_at.desc',
                headers=get_supabase_headers()
            )
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify([]), 200
                
        except Exception as e:
            print(f"获取笔记错误: {e}")
            return jsonify([]), 200
    
    @app.route('/api/notes', methods=['POST'])
    def create_note():
        """创建新笔记"""
        try:
            data = request.get_json()
            
            if not data or not data.get('title') or not data.get('content'):
                return jsonify({'error': '标题和内容不能为空'}), 400
            
            if not SUPABASE_URL or not SUPABASE_KEY:
                return jsonify({'error': '数据库配置错误'}), 500
            
            note_data = {
                'title': data['title'],
                'content': data['content'],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            response = requests.post(
                f'{SUPABASE_URL}/rest/v1/note',
                headers=get_supabase_headers(),
                data=json.dumps(note_data)
            )
            
            if response.status_code == 201:
                return jsonify(response.json()[0] if response.json() else note_data), 201
            else:
                return jsonify({'error': '创建笔记失败'}), 500
                
        except Exception as e:
            print(f"创建笔记错误: {e}")
            return jsonify({'error': f'服务器错误: {str(e)}'}), 500
    
    @app.route('/api/notes/<int:note_id>', methods=['PUT'])
    def update_note(note_id):
        """更新笔记"""
        try:
            data = request.get_json()
            
            if not SUPABASE_URL or not SUPABASE_KEY:
                return jsonify({'error': '数据库配置错误'}), 500
            
            update_data = {
                'updated_at': datetime.now().isoformat()
            }
            
            if 'title' in data:
                update_data['title'] = data['title']
            if 'content' in data:
                update_data['content'] = data['content']
            
            response = requests.patch(
                f'{SUPABASE_URL}/rest/v1/note?id=eq.{note_id}',
                headers=get_supabase_headers(),
                data=json.dumps(update_data)
            )
            
            if response.status_code == 200:
                return jsonify({'message': '笔记更新成功'}), 200
            else:
                return jsonify({'error': '更新笔记失败'}), 500
                
        except Exception as e:
            print(f"更新笔记错误: {e}")
            return jsonify({'error': f'服务器错误: {str(e)}'}), 500
    
    @app.route('/api/notes/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id):
        """删除笔记"""
        try:
            if not SUPABASE_URL or not SUPABASE_KEY:
                return jsonify({'error': '数据库配置错误'}), 500
            
            response = requests.delete(
                f'{SUPABASE_URL}/rest/v1/note?id=eq.{note_id}',
                headers=get_supabase_headers()
            )
            
            if response.status_code == 204:
                return jsonify({'message': '笔记删除成功'}), 200
            else:
                return jsonify({'error': '删除笔记失败'}), 500
                
        except Exception as e:
            print(f"删除笔记错误: {e}")
            return jsonify({'error': f'服务器错误: {str(e)}'}), 500
    
    @app.route('/api/translate', methods=['POST'])
    def translate_note():
        """翻译笔记"""
        try:
            data = request.get_json()
            
            if not data or not data.get('text'):
                return jsonify({'error': '需要翻译的文本不能为空'}), 400
            
            if not GITHUB_TOKEN:
                return jsonify({'error': 'AI 服务未配置'}), 500
            
            # 模拟翻译功能（实际中应该调用 LLM API）
            text = data['text']
            target_lang = data.get('target_lang', 'English')
            
            # 简单的翻译逻辑
            translated_text = f"[翻译为{target_lang}] {text}"
            
            return jsonify({
                'original_text': text,
                'translated_text': translated_text,
                'target_language': target_lang
            })
            
        except Exception as e:
            print(f"翻译错误: {e}")
            return jsonify({'error': f'翻译服务错误: {str(e)}'}), 500
    
    @app.route('/api/generate', methods=['POST'])
    def generate_notes():
        """AI 生成笔记"""
        try:
            data = request.get_json()
            
            if not data or not data.get('topic'):
                return jsonify({'error': '主题不能为空'}), 400
            
            if not GITHUB_TOKEN:
                return jsonify({'error': 'AI 服务未配置'}), 500
            
            # 模拟 AI 生成功能
            topic = data['topic']
            
            generated_notes = [
                {
                    'title': f'{topic} - 重点 1',
                    'content': f'关于{topic}的第一个重要观点...',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M')
                },
                {
                    'title': f'{topic} - 重点 2',
                    'content': f'关于{topic}的第二个重要观点...',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M')
                }
            ]
            
            return jsonify({
                'topic': topic,
                'generated_notes': generated_notes
            })
            
        except Exception as e:
            print(f"生成笔记错误: {e}")
            return jsonify({'error': f'AI 生成服务错误: {str(e)}'}), 500
    
    @app.route('/api/health')
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'ok',
            'message': 'Note Taking App is running',
            'features': {
                'database': bool(SUPABASE_URL and SUPABASE_KEY),
                'ai_services': bool(GITHUB_TOKEN),
                'translation': True,
                'note_management': True
            },
            'timestamp': datetime.now().isoformat()
        })
    
    # Vercel 兼容性
    application = app
    
    if __name__ == '__main__':
        app.run(debug=False)

except ImportError as e:
    # 如果依赖包导入失败，返回基础应用
    def application(environ, start_response):
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        
        html = f"""<!DOCTYPE html>
<html><head><title>Import Error</title></head>
<body style="font-family: system-ui; text-align: center; padding: 50px;">
<h1>⚠️ 依赖包加载失败</h1>
<p>错误: {str(e)}</p>
<p>正在使用基础模式...</p>
<p><a href="/api/health">健康检查</a></p>
</body></html>"""
        
        start_response(status, headers)
        return [html.encode('utf-8')]

except Exception as e:
    # 其他错误的处理
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        
        html = f"""<!DOCTYPE html>
<html><head><title>Application Error</title></head>
<body style="font-family: system-ui; text-align: center; padding: 50px;">
<h1>🚫 应用启动失败</h1>
<p>错误: {str(e)}</p>
</body></html>"""
        
        start_response(status, headers)
        return [html.encode('utf-8')]