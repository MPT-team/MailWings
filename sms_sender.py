from twilio.rest import Client


def send_sms(information, sms_body):
    account_sid = information['account_sid']
    auth_token = information['auth_token']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_body,
        from_=information['receiver_number'],
        to=information['sender_number']
    )

    print("LOGGER - INFO - SMS WAS SENT SID:", message.sid)
