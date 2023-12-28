import imaplib
import email
from datetime import datetime
from telegram_poc.telegram_notification import send_telegram_notification
from sms_notification import send_sms_notification
from openai import OpenAI


SLEEP_TIME = 5

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")
    else:
        body = msg.get_payload(decode=True).decode("utf-8")
    return body

def generate_openai_response(body, key):
    client = OpenAI(api_key=key)

    message = f"Hello, shorrten this mesage text {body} in one or two sentence. \
                Please in response provide mi only short version of this message \
                Also please do not provide message longer than one sentences."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": message},
        ]
    )

    return completion.choices[0].message.content

def check_emails(information, bot):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(information['user']['imap_host'], information['user']['imap_port'])
    now = datetime.now()
    print(f"LOGGER - INFO - [{now.strftime('%H:%M:%S')}] emails was checked")

    # Login to account
    mail.login(information['user']['username'], information['user']['password'])

    # Select the mailbox
    mail.select('inbox')

    # Search for all unseen emails
    result, data = mail.search(None, 'UNSEEN')

    if result == 'OK':
        for num in data[0].split():
            # Fetch the email by its number
            result, message_data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                # Parse the email message
                email_message = email.message_from_bytes(message_data[0][1])
                # Get the sender email address
                sender_email = email.utils.parseaddr(email_message['From'])[1]

                # Check if the sender email_module is in the priority list
                if sender_email in information['priority_emails']:
                    now = datetime.now()
                    subject = email_message['Subject']
                    body = get_email_body(email_message)
                    open_ai_response = generate_openai_response(body, information['openai'])

                    print(f"LOGGER - INFO - [{now.strftime('%H:%M:%S')}] PIORITY EMAIL WAS SEND {sender_email}")
                    
                    send_sms_notification(information, sender_email, subject, open_ai_response)
                    send_telegram_notification(information, sender_email, subject, bot, open_ai_response)
    # Logout
    mail.logout()
