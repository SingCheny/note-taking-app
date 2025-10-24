# Minimal Flask app for Vercel
import json
import os

def application(environ, start_response):
    """
    Ultra-minimal WSGI application for Vercel
    避免 Flask 导入和复杂依赖
    """
    try:
        # 获取请求路径
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')
        
        # 简单的HTML响应
        if path == '/' and method == 'GET':
            html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Note Taking App - Vercel Success</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255,255,255,0.18);
            text-align: center;
            max-width: 600px;
        }
        h1 { font-size: 2.5rem; margin-bottom: 20px; }
        .success { color: #4CAF50; font-size: 1.3rem; margin: 20px 0; }
        .status { 
            background: rgba(0,0,0,0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }
        .badge { 
            display: inline-block; 
            background: #4CAF50; 
            color: white; 
            padding: 5px 12px; 
            border-radius: 20px; 
            font-size: 0.9rem;
            margin: 5px;
        }
        .info { color: #81C784; font-weight: bold; }
        ul { text-align: left; margin: 20px 0; }
        li { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Note Taking App</h1>
        <div class="success">✅ Vercel 部署成功！</div>
        
        <div class="status">
            <p><span class="info">状态:</span> 应用正常运行</p>
            <p><span class="info">环境:</span> Vercel Serverless</p>
            <p><span class="info">版本:</span> Python 3.11</p>
        </div>
        
        <div class="badge">✅ 部署成功</div>
        <div class="badge">🚀 自动扩缩</div>
        <div class="badge">🔒 HTTPS</div>
        <div class="badge">🌐 全球CDN</div>
        
        <h3 style="margin: 30px 0 15px 0;">📋 开发状态</h3>
        <ul style="text-align: center; list-style: none;">
            <li>✅ 基础部署 - 完成</li>
            <li>🔄 功能集成 - 开发中</li>
            <li>🔄 数据库连接 - 准备中</li>
            <li>🔄 AI功能 - 计划中</li>
        </ul>
        
        <p style="margin-top: 30px; opacity: 0.9;">
            🎯 <strong>本地开发:</strong> localhost:5001 (完整功能)<br>
            🌍 <strong>生产环境:</strong> 当前URL (基础版本)
        </p>
    </div>
</body>
</html>"""
            
            status = '200 OK'
            headers = [
                ('Content-Type', 'text/html; charset=utf-8'),
                ('Cache-Control', 'no-cache'),
                ('X-Powered-By', 'Vercel + Python')
            ]
            
        elif path == '/api/health' and method == 'GET':
            # 健康检查端点
            response_data = {
                "status": "ok",
                "timestamp": os.environ.get('VERCEL_DEPLOYMENT_ID', 'local'),
                "region": os.environ.get('VERCEL_REGION', 'unknown'),
                "message": "Note Taking App is running successfully"
            }
            html = json.dumps(response_data)
            status = '200 OK'
            headers = [
                ('Content-Type', 'application/json'),
                ('Cache-Control', 'no-cache')
            ]
            
        else:
            # 404 页面
            html = """<!DOCTYPE html>
<html><head><title>404 - Not Found</title></head>
<body style="font-family: system-ui; text-align: center; padding: 50px;">
<h1>404 - Page Not Found</h1>
<p><a href="/">← Back to Home</a></p>
</body></html>"""
            status = '404 Not Found'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
        
        start_response(status, headers)
        return [html.encode('utf-8')]
        
    except Exception as e:
        # 错误处理
        error_html = f"""<!DOCTYPE html>
<html><head><title>Error</title></head>
<body style="font-family: system-ui; text-align: center; padding: 50px;">
<h1>Application Error</h1>
<p>Something went wrong: {str(e)}</p>
<p><a href="/">← Back to Home</a></p>
</body></html>"""
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_html.encode('utf-8')]

# Vercel 兼容性
app = application