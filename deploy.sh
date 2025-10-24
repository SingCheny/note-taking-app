#!/bin/bash
# Deployment script for Vercel

echo "🚀 Deploying Note Taking App to Vercel"
echo "======================================"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "🔧 Setting up environment variables..."

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📋 Post-deployment checklist:"
echo "1. ✅ RLS policies enabled in Supabase"
echo "2. ✅ Environment variables set"
echo "3. ✅ Application deployed"
echo ""
echo "🌐 Your app should be live at the provided URL!"