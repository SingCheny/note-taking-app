# Railway Deployment Guide

## 🚀 Railway 部署指南（Vercel 替代方案）

Railway 是一个免费的云平台，不需要信用卡或账单地址。

### 步骤：

1. **访问 Railway**: https://railway.app
2. **使用 GitHub 登录**
3. **创建新项目**: "Deploy from GitHub repo"
4. **选择仓库**: `note-taking-app-updated-SingCheny`
5. **添加环境变量**:
   ```
   GITHUB_TOKEN=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
   SUPABASE_URL=https://ujunndegjyuycbjtrutf.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqdW5uZGVnanl1eWNianRydXRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMTE3NDQsImV4cCI6MjA3Njg4Nzc0NH0.GL2LpaVca7co0nTs3AQJRPtBUI5fI1Fychbsye5_kk0
   FLASK_ENV=production
   PORT=8000
   ```
6. **部署完成**

### 优势：
- ✅ 完全免费
- ✅ 不需要信用卡
- ✅ 支持 Python
- ✅ 自动 HTTPS
- ✅ 简单设置