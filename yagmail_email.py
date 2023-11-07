import yagmail
from password import password

yag = yagmail.SMTP('info.mailwings', password)
to = 'kuba.tutka@wp.pl'
subject = 'Test mail subject with yagmail'
body = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut eu elit tempor diam mattis venenatis.
"""

yag.send(to = to, subject = subject, contents = body)