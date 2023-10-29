from twilio.rest import Client

# Dane uwierzytelniające
account_sid = '###'
auth_token = '###'

# Inicjalizacja klienta Twilio
client = Client(account_sid, auth_token)

# Wysyłanie wiadomości SMS
message = client.messages.create(
    body='ROKOKO TOP!!!',
    from_='###',
    to='###'
)

print("Wiadomość wysłana. SID:", message.sid)
