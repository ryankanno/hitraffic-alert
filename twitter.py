import settings

from twilio.rest import TwilioRestClient


def notify_via_twilio(to, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    client.messages.create(to=to, from_=from_number, body=message)
