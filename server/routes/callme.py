
import os
from dotenv import load_dotenv
from flask import jsonify
from flask import request
from server import app
from server.routes import prometheus
from twilio.rest import Client

# Initialize the Twilio client
#
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_phone_number = os.environ['TWILIO_PHONE_NUMBER']
client = Client(account_sid, auth_token)


@app.route("/api/v1/callme", methods=['POST'])
@prometheus.track_requests
def callme():
    """callme numbers route"""
    input = request.get_json(force=True)
    for i in input:
        name = i.get('name')
        phone = i['phone']
        message = i.get('message', 'Hi there')
        print("Call", name, "at", phone, "message:", message)
        call_via_twilio(phone, message)

    state = {"status": "Accepted"}
    return jsonify(state), 202


def call_via_twilio(to_phone_number, message):

    # TODO: auto-format the phone numbers to +5551238888 format

    try:
        message = client.messages.create(
            to=to_phone_number,
            from_=from_phone_number,
            body=message)
        print("Twilio message SID:", message.sid)
    except Exception as e:
        print(e)
