#!/usr/bin/env python3
"""
本地测试 Vercel 应用
"""

import sys
import os
from wsgiref.simple_server import make_server
from urllib.parse import urlparse, parse_qs

# 添加 api 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

try:
    from index import application
    
    def run_server():
        """运行本地测试服务器"""
        port = 8000
        
        # 设置环境变量模拟 Vercel 环境
        os.environ['VERCEL_ENV'] = 'development'
        os.environ['VERCEL_REGION'] = 'local'
        
        # 如果有 .env 文件，加载它
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        print(f"""
🚀 启动 Vercel 应用本地测试服务器
========================================
🌐 URL: http://localhost:{port}
🔧 环境: {os.environ.get('VERCEL_ENV', 'local')}
🗄️ 数据库: {'✅ 已配置' if os.environ.get('SUPABASE_URL') else '❌ 未配置'}
📱 功能: 笔记管理, 搜索, 翻译

按 Ctrl+C 停止服务器
========================================
        """)
        
        with make_server('', port, application) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n👋 服务器已停止")

    if __name__ == '__main__':
        run_server()
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保在正确的目录中运行此脚本")
except Exception as e:
    print(f"❌ 启动失败: {e}")