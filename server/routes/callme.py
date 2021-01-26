
import datetime
import os
import queue
import random
import threading
import time

from flask import jsonify
from flask import request
from server import app
from server.routes import prometheus
from twilio.rest import Client

from server.config import db

# Initialize the Twilio client
#
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

sleep_min = int(os.environ.get('CALL_SLEEP_MIN', 1))
sleep_max = int(os.environ.get('CALL_SLEEP_MAX', 10))

client = None
if account_sid and auth_token and from_phone_number:
    client = Client(account_sid, auth_token)

# Queue and tasks for calling to add random wait times between calls
q = queue.Queue()


def caller():
    while True:
        callee = q.get()
        print('Begin calling:', callee)
        phone = callee[0]
        msg = callee[1]
        posted = callee[2]
        call_via_twilio(phone, msg)
        print('Done texting "', msg, '" to', phone)

        db.insert_call_me(
            {
                'PHONE': phone[1:],
                'POSTED': posted,
                'CALLED': datetime.datetime.now()
            }
        )

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
    call_these = request.get_json(force=True)
    for i in call_these:
        name = i.get('name')
        digits = ''.join(n for n in i['phone'] if n.isdigit())
        prefix = '+1' if len(digits) == 10 else '+'
        phone = prefix + digits
        message = i.get('message', random.choice(hellos))
        print("POST", name, "at", phone, "message:", message)
        q.put((phone, message, datetime.datetime.now()))

    state = {"status": "Accepted"}
    return jsonify(state), 202


def call_via_twilio(to_phone_number, message):

    if not client:
        print("--> Skipping Twilio call because it is not configured. <--")
        return

    try:
        message = client.messages.create(
            to=to_phone_number,
            from_=from_phone_number,
            body=message)
        print("Twilio message SID:", message.sid)
        print("Twilio message:", message)
    except Exception as e:
        print(e)
