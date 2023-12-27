from jinja2 import Environment, FileSystemLoader

def render_template(template_path, data):
    env = Environment(loader=FileSystemLoader('.'))

    template = env.get_template(template_path)

    return template.render(data)

def send_telegram_notification(information, sender_email, subject, bot, open_ai_response):
    # variables
    template_file_path = 'templates/notification_template.jinja'

    data = {
        "subject": subject,
        "recipient_name": information['name'],
        "sender_name": sender_email,
        "dev_name": "MailWings team",
        "open_ai_response": open_ai_response
    }

    # template rendering
    message_content = render_template(template_file_path, data)

    bot.send_message(information['chat_id'], message_content)

    print("LOGGER - INFO - TELEGRAM INFO WAS SEND")