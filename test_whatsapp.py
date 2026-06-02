from twilio.rest import Client

account_sid = 'TON_ACCOUNT_SID'
auth_token = 'TON_AUTH_TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Bienvenue sur Y4thLink 🌿 Tes questions restent privées. Tape : info, rdv, clinique ou conseiller',
    to='whatsapp:+22963091714'
)

print("Message envoyé ! SID:", message.sid)
