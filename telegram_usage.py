from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler, \
    CallbackContext
import telebot
import threading
import time
from email_listener import check_emails, SLEEP_TIME
from database_info import get_database_information, add_priority_mail, delete_priority_mail

ADD_EMAIL, DELETE_EMAIL, LOGIN = range(3)

# DB z bazy zczytujemy wszystkie potrzebne info o userze

information = get_database_information()
bot = telebot.TeleBot(token=information['token'])


# POOLING

def email_polling():
    while not stop_email_pooling_list[-1].is_set():
        check_emails(information, bot)
        time.sleep(SLEEP_TIME)


stop_email_pooling_list = []
email_pooling_list = []


# HANDLERS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("LOGGER - INFO - Login process begin")
    await update.message.reply_text('Hello to MailWings!\
                                    Please type your password')

    return LOGIN


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'To start monitoring your high-priority emails send or press /start \nTo add high-priority mail send or press /add \nTo delete high-priority mail write or press /delete \nTo show all high-priority mails write or press /show')


async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_email_pooling_list[-1].set()
    email_pooling_list[-1].join()
    print("LOGGER - INFO - Monitoring pioritized mails is stopped")
    await update.message.reply_text('Thanks for using our feature. See you soon!')


async def show_prioritized_emails_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("LOGGER - INFO - Emails show command start")

    response = ""

    for pioritized_email in information['priority_emails']:
        response += str(pioritized_email) + "\n"

    await update.message.reply_text('This is the list of your high-priority emails:')
    await update.message.reply_text(response)


async def add_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("LOGGER - INFO - Email add command start")
    await update.message.reply_text('Please write the email which you want to add.')

    return ADD_EMAIL


async def delete_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("LOGGER - INFO - Email delete command start")

    response = ""

    for pioritized_email in information['priority_emails']:
        response += str(pioritized_email) + "\n"

    await update.message.reply_text('Please write the email which you want to delete.')
    await update.message.reply_text(response)

    return DELETE_EMAIL


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'LOGGER - INFO - Update {update} caused error {context.error}')


async def start_email_polling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text: str = update.message.text

    bot.delete_message(information['configuration_chat_id'], update.message.id)
    response = "Password was entered"

    if hash(text) == hash(information['password']):
        stop_email_pooling_list.append(threading.Event())
        email_pooling_list.append(threading.Thread(target=email_polling))
        email_pooling_list[-1].start()
        response = "Correct password, cheaking email is started"
    else:
        response = "Wrong password - plase try again later"

    await update.message.reply_text(response)

    print(f'LOGGER - INFO - MailWings ({update.message.chat.id}) in: {hash(response)}')

    return ConversationHandler.END


async def add_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) wants to add email: "{text}"')

    if text:
        information['priority_emails'].append(text)
        add_priority_mail(text)
        response = "Mail successfully added to prioritized emails!"
    else:
        response = "Something went wrong, try one more time by executing /add"

    await update.message.reply_text(response)

    print(f'LOGGER - INFO - MailWings ({update.message.chat.id}) in: {response}')

    return ConversationHandler.END


async def delete_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text: str = update.message.text
    print(f'LOGGER - INFO - User ({update.message.chat.id}) wants to delete email: "{text}"')

    for pioritized_email in information['priority_emails']:
        if text == pioritized_email:
            information['priority_emails'].remove(text)
            delete_priority_mail(text)
            response = "Mail successfully deleted from prioritized emails!"
            break
        else:
            response = "Something went wrong, try one more time by executing /delete"

    await update.message.reply_text(response)

    print(f'MailWings ({update.message.chat.id}) in: {response}')

    return ConversationHandler.END


async def wrong_email_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = "You entered the wrong structure of the email, e.g., without @. Try one more time by typing /add!"

    await update.message.reply_text(response)

    print(f'MailWings ({update.message.chat.id}) in: {response}')

    return ConversationHandler.END


async def wrong_email_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = "You entered the wrong structure of the email, e.g., without @. Try one more time by typing /delete!"

    await update.message.reply_text(response)

    print(f'LOGGER - INFO - MailWings ({update.message.chat.id}) in: {response}')

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Something went wrong.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


# INITIALIZATION

def initialize_app():
    print("LOGGER - INFO - Start MailWings application")

    for handler in handlers:
        app.add_handler(handler)

    app.add_error_handler(error)

    app.run_polling(poll_interval=3)


def initialize_handlers():
    handlers = [
        CommandHandler('help', help_command),
        CommandHandler('show', show_prioritized_emails_command),
        CommandHandler('end', end_command)
    ]

    start_email_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            LOGIN: [MessageHandler(filters.TEXT, start_email_polling)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    add_email_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_email_command)],
        states={
            ADD_EMAIL: [MessageHandler(filters.Regex(".*@.*"), add_email),
                        MessageHandler(filters.Regex("^(?!.*@.*$).*"), wrong_email_add)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    delete_email_handler = ConversationHandler(
        entry_points=[CommandHandler('delete', delete_email_command)],
        states={
            DELETE_EMAIL: [MessageHandler(filters.Regex(".*@.*"), delete_email),
                           MessageHandler(filters.Regex("^(?!.*@.*$).*"), wrong_email_delete)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    handlers.append(start_email_handler)
    handlers.append(delete_email_handler)
    handlers.append(add_email_handler)

    return handlers


# SECURITY

def delete_last_message(update: Update, context: CallbackContext):
    global last_message_id
    if last_message_id:
        update.message.bot.delete_message(update.message.chat_id, last_message_id)
        last_message_id = None
    else:
        update.message.reply_text("No messages to delete.")


if __name__ == '__main__':
    delete_priority_mail("cos@gmail.com")
    handlers = initialize_handlers()
    delete_priority_mail("cos@gmail.com")
    app = Application.builder().token(information['token']).build()

    initialize_app()
