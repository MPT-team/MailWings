import imaplib
import email
from secret import password
from email.header import decode_header


port = 993
imap_server = 'imap.gmail.com'
email_address = 'info.mailwings@gmail.com'

mail = imaplib.IMAP4_SSL(imap_server)
mail.login(email_address, password)

mail.select("Inbox")

status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    email_message = email.message_from_bytes(msg_data[0][1])
    subject, encoding = decode_header(email_message["Subject"])[0]

    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')

    from_address = email.utils.parseaddr(email_message.get("From"))[1]
    date_sent = email_message["Date"]

    print(f"Subject: {subject}")
    print(f"From: {from_address}")
    print(f"Date: {date_sent}")

    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                print(f"Body:\n{body.decode('utf-8')}")

mail.close()
mail.logout()