# Vercel 部署指南

## 📋 **部署前准备清单**

### ✅ **步骤 1: 修复 Supabase 安全设置**
1. 访问: https://supabase.com/dashboard
2. 选择项目: `ujunndegjyuycbjtrutf`
3. 进入 SQL Editor
4. 运行 fix_supabase_security.py 输出的 SQL 命令

### ✅ **步骤 2: Vercel 环境变量设置**

在 Vercel Dashboard 中设置以下环境变量:

```
DATABASE_URL=postgresql://postgres:Csy900207@db.ujunndegjyuycbjtrutf.supabase.co:5432/postgres

SUPABASE_URL=https://ujunndegjyuycbjtrutf.supabase.co

SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqdW5uZGVnanl1eWNianRydXRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMTE3NDQsImV4cCI6MjA3Njg4Nzc0NH0.GL2LpaVca7co0nTs3AQJRPtBUI5fI1Fychbsye5_kk0

GITHUB_TOKEN=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

FLASK_ENV=production

SECRET_KEY=production-secret-key-change-this-in-production
```

### ✅ **步骤 3: 部署命令**

```bash
# 安装 Vercel CLI (如果还没有)
npm install -g vercel

# 登录 Vercel
vercel login

# 部署
vercel --prod
```

### ✅ **步骤 4: 验证部署**

部署完成后:
1. 检查应用是否正常加载
2. 测试创建笔记功能
3. 测试翻译功能
4. 测试 LLM 生成功能
5. 检查 Supabase 中的数据

## 🚨 **故障排除**

### 如果遇到数据库连接问题:
1. 检查 Supabase 项目是否处于活跃状态
2. 验证 DATABASE_URL 格式正确
3. 确认 RLS 策略已启用

### 如果遇到 LLM 功能问题:
1. 检查 GITHUB_TOKEN 是否有效
2. 验证网络连接到 GitHub Models

### 如果遇到静态文件问题:
1. 检查 vercel.json 配置
2. 验证 static 文件夹结构