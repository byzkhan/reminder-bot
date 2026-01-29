#!/bin/bash

# Quick Start Script for Reminder Bot
# ====================================

echo "🔔 Persistent Reminder Bot"
echo "=========================="
echo ""

# Check if token is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your Telegram bot token!"
    echo ""
    echo "Usage: ./run.sh YOUR_BOT_TOKEN"
    echo ""
    echo "Example: ./run.sh 123456789:ABCdefGHI..."
    exit 1
fi

# Set the token
export TELEGRAM_BOT_TOKEN="$1"

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Starting bot..."
echo ""

# Run the bot
python bot.py
