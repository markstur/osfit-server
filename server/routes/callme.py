
import os
from dotenv import load_dotenv
from flask import jsonify
from flask import request
import random
from server import app
from server.routes import prometheus
from twilio.rest import Client
import threading
import time
import queue

# Initialize the Twilio client
#
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
load_dotenv()
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
sleep_min = os.environ.get('SLEEP_MIN', 1)
sleep_max = os.environ.get('SLEEP_MAX', 10)
client = Client(account_sid, auth_token)

# Queue and tasks for calling to add random wait times between calls
q = queue.Queue()

def caller():
  while True:
    callee = q.get()
    print('Begin calling:', callee)
    call_via_twilio(callee[0], callee[1])
    print('Done texting "', callee[1], '" to', callee[0])
    s = random.randint(sleep_min, sleep_max)
    print('Wait ', s, 'seconds')
    time.sleep(s)
    q.task_done()

threading.Thread(target=caller, daemon=True).start()

# Random initial text message
hellos = [
  'Hi there',
  'Howdy',
  'Hi',
  'Hey'
]

@app.route("/api/v1/callme", methods=['POST'])
@prometheus.track_requests
def callme():
    """callme numbers route"""
    input = request.get_json(force=True)
    for i in input:
        name = i.get('name')
        digits = ''.join(n for n in i['phone'] if n.isdigit())
        prefix = '+1' if len(digits) == 10 else '+'
        phone = prefix + digits
        message = i.get('message', random.choice(hellos))
        print("POST", name, "at", phone, "message:", message)
        # call_via_twilio(phone, message)
        q.put((phone, message))

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
