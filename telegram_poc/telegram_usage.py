from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import telebot



# notifications

def send_notification():
    bot = telebot.TeleBot(token=TOKEN)
    bot.send_message(CHAT_ID, 'Hi! I\'m a Bot!')

# commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello to MailWings!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How can I help You?')

async def prioritized_emails_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SELECT * FROM EMAILS WHERE EMAILS.uid = TOKEN
    await update.message.reply_text('This is list of your high-priority emails:')

async def add_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SELECT * FROM EMAILS WHERE EMAILS.uid = TOKEN
    await update.message.reply_text('To add email_module to high-priority list type: add email_module')

async def delete_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SELECT * FROM EMAILS WHERE EMAILS.uid = TOKEN
    await update.message.reply_text('To delete email_module from high-priority list type: delete email_module')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# responses

def handle_responses(text: str) -> str:

    print("**********", text)

    if 'hej' in text:
        return 'Co tam wariacie'
    
    return 'I do not know what you want from me :(, try one more time'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =  update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        new_text = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_responses(new_text)
    else:
        response: str = handle_responses(text)

    print('Bot:', response)

    await update.message.reply_text(response)

# logging and opperation

def initialize_app():

    print("Start aplication")
    
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('show', prioritized_emails_command))
    app.add_handler(CommandHandler('add', add_email_command))
    app.add_handler(CommandHandler('delete', delete_email_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    initialize_app()