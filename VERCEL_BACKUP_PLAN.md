# Vercel 部署备用方案

## 方案 1: 通过 Vercel CLI (当前尝试)
1. 访问: https://vercel.com/oauth/device?user_code=WDSF-XNGM
2. 登录并授权
3. 回到终端按 ENTER

## 方案 2: 通过 Vercel Dashboard (GitHub 集成)

### 步骤：
1. **推送代码到 GitHub** (如果还没有):
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **通过 Vercel Dashboard 导入**:
   - 访问: https://vercel.com/dashboard
   - 点击 "Add New..." → "Project"
   - 选择 "Import Git Repository"
   - 连接你的 GitHub 账户
   - 选择 `note-taking-app-updated-SingCheny` 仓库
   - Framework Preset: 选择 "Other"
   - Root Directory: 保持默认 "./"
   - Build Command: 留空 (我们使用 vercel.json 配置)
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`

3. **设置环境变量** (在 Vercel Dashboard):
   ```
   DATABASE_URL=postgresql://postgres:Csy900207@db.ujunndegjyuycbjtrutf.supabase.co:5432/postgres
   SUPABASE_URL=https://ujunndegjyuycbjtrutf.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqdW5uZGVnanl1eWNianRydXRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMTE3NDQsImV4cCI6MjA3Njg4Nzc0NH0.GL2LpaVca7co0nTs3AQJRPtBUI5fI1Fychbsye5_kk0
   GITHUB_TOKEN=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
   FLASK_ENV=production
   ```

4. **部署**: 点击 "Deploy"

## 推荐: 先尝试完成 CLI 登录，如果不行就使用方案 2