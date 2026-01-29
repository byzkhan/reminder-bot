# 🔔 Persistent Reminder Bot - Setup Guide

This guide will walk you through setting up your Telegram reminder bot **step by step**. No coding experience needed!

---

## 📋 What You'll Do

1. Create a Telegram bot (5 minutes)
2. Get your bot's token (1 minute)
3. Run the bot using Claude Code (2 minutes)

**Total time: ~10 minutes**

---

## Step 1: Create Your Telegram Bot

### 1.1 Open Telegram

Open Telegram on your phone or computer (desktop app or web.telegram.org)

### 1.2 Find BotFather

1. In Telegram, tap the **search icon** 🔍
2. Type: `@BotFather`
3. Click on the verified **BotFather** account (it has a blue checkmark ✓)

### 1.3 Create a New Bot

1. Click **Start** or type `/start`
2. Type `/newbot` and send it
3. BotFather will ask for a **name** for your bot
   - Type something like: `My Reminder Bot`
4. BotFather will ask for a **username** for your bot
   - This must end in `bot`
   - Type something like: `myreminders_bot` or `john_reminder_bot`
   - If it's taken, try adding numbers: `myreminders123_bot`

### 1.4 Save Your Token

After creating the bot, BotFather will give you a message like:

```
Done! Congratulations on your new bot. You will find it at t.me/yourbot_username.

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456789
```

⚠️ **IMPORTANT:** Copy that long token (the part that looks like `123456789:ABC...`). You'll need it in Step 3!

---

## Step 2: Start a Chat with Your Bot

1. Click the link BotFather gave you (like `t.me/yourbot_username`)
2. Click **Start** to begin chatting with your bot
3. This is important! The bot can only message you after you've started a chat with it.

---

## Step 3: Run the Bot with Claude Code

### Option A: Run Locally with Claude Code (Easiest)

Open Claude Code in your terminal and say:

```
Run the reminder bot from /home/claude/reminder-bot with my token: YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token from Step 1.4

### Option B: Run It Yourself

If you want to run it manually:

1. **Open your terminal** (Command Prompt on Windows, Terminal on Mac)

2. **Navigate to the bot folder:**
   ```bash
   cd /path/to/reminder-bot
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your bot token:**
   
   On Mac/Linux:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token_here"
   ```
   
   On Windows:
   ```bash
   set TELEGRAM_BOT_TOKEN=your_token_here
   ```

5. **Run the bot:**
   ```bash
   python bot.py
   ```

You should see:
```
🚀 Starting Persistent Reminder Bot...
⏰ Reminder interval: 20 minutes
✅ Bot is running! Press Ctrl+C to stop.
```

---

## Step 4: Use Your Bot!

Go back to Telegram and chat with your bot:

### Add a reminder:
```
/add Take my vitamins
```

### See all reminders:
```
/list
```

### Mark as done:
```
/done 1
```

### Remove a reminder:
```
/remove 1
```

---

## 🎉 That's It!

Your bot will now:
- ✅ Send you reminders every 20 minutes
- ✅ Keep nagging until you mark them done
- ✅ Let you click buttons or type commands to mark done

---

## ❓ Troubleshooting

### "Bot not responding"
- Make sure you clicked "Start" in your chat with the bot
- Make sure the bot is running (check your terminal)

### "Invalid token"
- Double-check you copied the entire token from BotFather
- Make sure there are no extra spaces

### "Module not found"
- Run `pip install -r requirements.txt` again

---

## 🌐 Want It Running 24/7?

The bot only works while your computer is on. For 24/7 operation, you can deploy to a free service. Ask Claude Code:

```
Help me deploy my reminder bot to Render.com for free
```

---

## 🔧 Customization

### Change reminder interval

In `bot.py`, find this line near the top:
```python
REMINDER_INTERVAL_MINUTES = 20
```

Change `20` to however many minutes you want between reminders.

---

## Need Help?

Just ask Claude Code! Say something like:
- "My reminder bot isn't working, help me debug"
- "How do I change the reminder interval to 10 minutes?"
- "Help me deploy this bot to run 24/7"
