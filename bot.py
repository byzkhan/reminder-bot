"""
Persistent Reminder Bot for Telegram
=====================================
This bot sends you reminders at the top of every hour until you mark them as done.

Setup instructions are in SETUP.md
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# === CONFIGURATION ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
REMINDER_INTERVAL_MINUTES = 60  # How often to nag you (every hour)
DATA_FILE = "reminders.json"

# === DATA STORAGE ===
def load_reminders():
    """Load reminders from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(data):
    """Save reminders to file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Global reminders storage: {user_id: {reminder_id: {text, active, created}}}
reminders = load_reminders()

# === HELPER FUNCTIONS ===
def get_user_reminders(user_id: str) -> dict:
    """Get all reminders for a user"""
    return reminders.get(str(user_id), {})

def generate_reminder_id() -> str:
    """Generate a unique reminder ID"""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

# === BOT COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message when user starts the bot"""
    welcome_text = """
🔔 **Welcome to Persistent Reminder Bot!**

I'll nag you at the top of every hour until you complete your tasks!

**Commands:**
• `/add <reminder>` - Add a new reminder
• `/list` - See all active reminders
• `/done <number>` - Mark a reminder as done
• `/remove <number>` - Delete a reminder
• `/help` - Show this help message

**Example:**
`/add Take my vitamins`
`/add Call mom`
`/add Drink water`

I'll keep reminding you every hour until you mark them done! 💪
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    await start(update, context)

async def add_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new reminder"""
    user_id = str(update.effective_user.id)
    
    # Get the reminder text from the command
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a reminder text!\n\nExample: `/add Take my medicine`",
            parse_mode="Markdown"
        )
        return
    
    reminder_text = " ".join(context.args)
    reminder_id = generate_reminder_id()
    
    # Initialize user's reminders if needed
    if user_id not in reminders:
        reminders[user_id] = {}
    
    # Add the reminder
    reminders[user_id][reminder_id] = {
        "text": reminder_text,
        "active": True,
        "created": datetime.now().isoformat(),
        "last_reminded": None
    }
    
    save_reminders(reminders)
    
    # Count active reminders for this user
    active_count = sum(1 for r in reminders[user_id].values() if r["active"])
    
    await update.message.reply_text(
        f"✅ **Reminder added!**\n\n"
        f"📝 \"{reminder_text}\"\n\n"
        f"I'll remind you at the top of every hour until you mark it done.\n"
        f"You have {active_count} active reminder(s).",
        parse_mode="Markdown"
    )

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all active reminders"""
    user_id = str(update.effective_user.id)
    user_reminders = get_user_reminders(user_id)
    
    active_reminders = [(rid, r) for rid, r in user_reminders.items() if r["active"]]
    
    if not active_reminders:
        await update.message.reply_text(
            "📭 You have no active reminders!\n\nUse `/add <reminder>` to create one.",
            parse_mode="Markdown"
        )
        return
    
    message = "📋 **Your Active Reminders:**\n\n"
    for i, (rid, reminder) in enumerate(active_reminders, 1):
        message += f"**{i}.** {reminder['text']}\n"
    
    message += f"\n_Use `/done <number>` to mark as complete_"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def mark_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark a reminder as done"""
    user_id = str(update.effective_user.id)
    user_reminders = get_user_reminders(user_id)
    
    if not context.args:
        await update.message.reply_text(
            "❌ Please specify which reminder number to mark done!\n\nExample: `/done 1`",
            parse_mode="Markdown"
        )
        return
    
    try:
        reminder_num = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number!")
        return
    
    active_reminders = [(rid, r) for rid, r in user_reminders.items() if r["active"]]
    
    if reminder_num < 1 or reminder_num > len(active_reminders):
        await update.message.reply_text(
            f"❌ Invalid reminder number! You have {len(active_reminders)} active reminder(s)."
        )
        return
    
    # Mark the reminder as done
    reminder_id, reminder = active_reminders[reminder_num - 1]
    reminders[user_id][reminder_id]["active"] = False
    save_reminders(reminders)
    
    remaining = sum(1 for r in reminders[user_id].values() if r["active"])
    
    await update.message.reply_text(
        f"🎉 **Great job!**\n\n"
        f"✅ Marked as done: \"{reminder['text']}\"\n\n"
        f"You have {remaining} reminder(s) left.",
        parse_mode="Markdown"
    )

async def done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the 'Done' button click from reminder notifications"""
    query = update.callback_query
    await query.answer()
    
    # Parse callback data: "done:user_id:reminder_id"
    _, user_id, reminder_id = query.data.split(":")
    
    if user_id in reminders and reminder_id in reminders[user_id]:
        reminder_text = reminders[user_id][reminder_id]["text"]
        reminders[user_id][reminder_id]["active"] = False
        save_reminders(reminders)
        
        remaining = sum(1 for r in reminders[user_id].values() if r["active"])
        
        await query.edit_message_text(
            f"🎉 **Great job!**\n\n"
            f"✅ Marked as done: \"{reminder_text}\"\n\n"
            f"You have {remaining} reminder(s) left.",
            parse_mode="Markdown"
        )

async def remove_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove a reminder completely"""
    user_id = str(update.effective_user.id)
    user_reminders = get_user_reminders(user_id)
    
    if not context.args:
        await update.message.reply_text(
            "❌ Please specify which reminder number to remove!\n\nExample: `/remove 1`",
            parse_mode="Markdown"
        )
        return
    
    try:
        reminder_num = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number!")
        return
    
    active_reminders = [(rid, r) for rid, r in user_reminders.items() if r["active"]]
    
    if reminder_num < 1 or reminder_num > len(active_reminders):
        await update.message.reply_text(
            f"❌ Invalid reminder number! You have {len(active_reminders)} active reminder(s)."
        )
        return
    
    # Remove the reminder
    reminder_id, reminder = active_reminders[reminder_num - 1]
    del reminders[user_id][reminder_id]
    save_reminders(reminders)
    
    await update.message.reply_text(
        f"🗑️ Removed: \"{reminder['text']}\"",
        parse_mode="Markdown"
    )

# === REMINDER LOOP ===
async def send_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Send reminders to all users with active reminders"""
    for user_id, user_reminders in reminders.items():
        active_reminders = [(rid, r) for rid, r in user_reminders.items() if r["active"]]
        
        if not active_reminders:
            continue
        
        # Build reminder message
        message = "⏰ **REMINDER TIME!**\n\n"
        message += "You still need to:\n\n"
        
        keyboard = []
        for i, (rid, reminder) in enumerate(active_reminders, 1):
            message += f"**{i}.** {reminder['text']}\n"
            # Add a "Done" button for each reminder
            keyboard.append([
                InlineKeyboardButton(
                    f"✅ Done: {reminder['text'][:20]}{'...' if len(reminder['text']) > 20 else ''}",
                    callback_data=f"done:{user_id}:{rid}"
                )
            ])
        
        message += f"\n_Click a button when done, or use `/done <number>`_"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await context.bot.send_message(
                chat_id=int(user_id),
                text=message,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            print(f"[{datetime.now()}] Sent reminder to user {user_id}")
        except Exception as e:
            print(f"[{datetime.now()}] Failed to send reminder to {user_id}: {e}")

# === MAIN ===
def main():
    """Start the bot"""
    print("🚀 Starting Persistent Reminder Bot...")
    print(f"⏰ Reminder interval: {REMINDER_INTERVAL_MINUTES} minutes")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_reminder))
    application.add_handler(CommandHandler("list", list_reminders))
    application.add_handler(CommandHandler("done", mark_done))
    application.add_handler(CommandHandler("remove", remove_reminder))
    
    # Add callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(done_callback, pattern="^done:"))
    
    # Set up the reminder job to run at the top of every hour
    job_queue = application.job_queue

    # Calculate seconds until the next top of hour
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    seconds_until_next_hour = (next_hour - now).total_seconds()

    job_queue.run_repeating(
        send_reminders,
        interval=timedelta(minutes=REMINDER_INTERVAL_MINUTES),
        first=timedelta(seconds=seconds_until_next_hour)  # First reminder at top of next hour
    )
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
