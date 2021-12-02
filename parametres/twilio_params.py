from twilio.rest import Client
from django.conf import settings

# account_sid = 'ACa9b3a79bcacc0ec38c29135fc5e395d1'
# auth_token = '85aa55fb1024bfe53a8d05104af76b91'

account_sid = 'ACf9539e42d9b32b5c9b190237d6a3ae35'
auth_token = '6b68266f48c0cde4d5d81453a4eade47'
client = Client(account_sid, auth_token)

def verifications(phone_number, via):
        return client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel=via)

def verification_checks(phone_number, token):
        return client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verification_checks.create(to=phone_number, code=token)