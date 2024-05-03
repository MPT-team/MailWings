from render.render_data import render_template
from render.read_config import read_config
from sms_sender import send_sms

# variables
template_file_path = 'templates/sms_notification_template.jinja'
config_file_path = 'configs/sms_config.ini'

# reading sms config
config = read_config(config_file_path)

# tutaj będzie plik konifguracyjny/zmienne przekazywane po zaimplementowaniu tego api od kalendarza/maila
mail_subject = "WAŻNY EMAIL"
recipient_name = "ROKOKO"
sender_name = "roko123@gmail.com"
dev_name = "Zespół MailWings"

data = {
    "subject": mail_subject,
    "recipient_name": recipient_name,
    "sender_name": sender_name,
    "dev_name": dev_name
}

# template rendering
message_content = render_template(template_file_path, data)

# sending sms
send_sms(config, message_content)
