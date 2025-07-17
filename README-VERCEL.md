# Free 24/7 Telegram Bot on Vercel

This is a cost-effective alternative to expensive hosting plans. Your bot will run completely FREE on Vercel.

## How to Deploy for FREE on Vercel:

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub (free)

### Step 2: Deploy Your Bot
1. Fork this project to your GitHub
2. In Vercel, click "New Project"
3. Import from GitHub
4. Select this repository

### Step 3: Configure Environment Variables
In Vercel project settings, add:
- `TELEGRAM_BOT_TOKEN` = your bot token from @BotFather

### Step 4: Set Webhook
After deployment, you'll get a URL like: `https://your-project.vercel.app`

Run this command (replace with your details):
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-project.vercel.app/api/webhook"}'
```

## Benefits:
- ✅ **Completely FREE** hosting
- ✅ **24/7 uptime** with serverless architecture  
- ✅ **Auto-scaling** - handles any amount of traffic
- ✅ **No $25/month fees** - saves you $300/year!
- ✅ **Global CDN** for fast responses worldwide
- ✅ **HTTPS included** automatically

## Your Bot Commands:
- `/start` - Welcome message
- `/help` - Help and information  
- `/status` - Bot status
- `/ping` - Test responsiveness

## Cost Comparison:
- **Replit Reserved VM**: $25/month = $300/year
- **Vercel Serverless**: $0/month = $0/year
- **Savings**: $300/year!

Your bot will work exactly the same but cost nothing to run!