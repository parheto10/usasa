# import vonage

# client = vonage.Client(key='cfc77dae', secret="wYBHLRbzyVjDDtS4")
# sms = vonage.Sms(client)
#
# responseData = sms.send_message(
#     {
#         "from": "GHS-HOLDING",
#         "to": "33756227336",
#         "text": "Bienvenus Sur GHS - HOLDING",
#     }
# )
#
# if responseData["messages"][0]["status"] == "0":
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
from twilio.rest import Client

account_sid = 'AC7538f3cd9e32c282bfe2794c300d3a1b'
auth_token = 'a203471476d1f63807e60883fee01140'
client = Client(account_sid, auth_token)

message = client.messages.create(
    messaging_service_sid='MG46bede6f533c252fa1e9843bde7f74aa',
    body='bienvenus sur GHS',
    to='+2250748566846'
)

print(message.sid)

