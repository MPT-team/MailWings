from secret import password, priority_email_example
import imaplib
import email
import time
from datetime import datetime

SLEEP_TIME = 5

PRIORITY_EMAILS = [
    priority_email_example
]

user = {
    'username': 'info.mailwings@gmail.com',
    'password': password,
    'imap_host': 'imap.gmail.com',
    'imap_port': 993
}


def check_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(user['imap_host'], user['imap_port'])
    now = datetime.now()
    print(f"[{now.strftime('%H:%M:%S')}] EMAIL CHECK")

    # Login to account
    mail.login(user['username'], user['password'])

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
                if sender_email in PRIORITY_EMAILS:
                    now = datetime.now()
                    subject = email_message['Subject']
                    print('*' * 10)
                    print(f"{now.strftime('%H:%M:%S')}] Priority Email received from {sender_email}")
                    print(f"Subject: {subject}")
                    print('*' * 10)

    # Logout
    mail.logout()


while True:
    check_emails()
    # Wait for SLEEP_TIME seconds before checking again
    time.sleep(SLEEP_TIME)
