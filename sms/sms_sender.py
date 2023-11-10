from twilio.rest import Client


def send_sms(config_file, sms_body):
    account_sid = config_file.get('Settings', 'account_sid')
    auth_token = config_file.get('Settings', 'auth_token')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_body,
        from_=config_file.get('Settings', 'sender_number'),
        to=config_file.get('Settings', 'receiver_number')
    )

    print("Wiadomość wysłana. SID:", message.sid)
