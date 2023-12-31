from secret import password
from email_module.message import EmailMessage
import ssl
import smtplib

email_sender = 'info.mailwings@gmail.com'
email_password = password
email_receiver = 'kuba.tutka@wp.pl'

subject = "Test mail subject"
body = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut eu elit tempor diam mattis venenatis.
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())