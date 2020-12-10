
import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import jsonify
from flask import request
from ibm_watson import DiscoveryV1
from server import app
from server.routes import prometheus

# Initialize the Discovery client
#
load_dotenv()
DISCOVERY_PROJECT_ID = os.environ.get('DISCOVERY_PROJECT_ID')
DISCOVERY_ENVIRONMENT_ID = os.environ.get('DISCOVERY_ENVIRONMENT_ID')
discovery = DiscoveryV1(version='2020-12-08')


@app.route("/api/v1/crawlme", methods=['POST'])
@prometheus.track_requests
def crawlme():
    """crawlme url route"""
    input = request.get_json(force=True)
    print("INPUT:", input)
    crawl_url(input.get('url'))

    state = {"status": "Accepted"}
    return jsonify(state), 202


def crawl_url(url):
    print("Crawlme url:", url)
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
        return

    soup = BeautifulSoup(page.text)  # , 'lxml')
    for link in soup.find_all('a'):
        print(link.get('href'))
    send_to_discovery(page.text)


def send_to_discovery(text_io):

    print("text_io type:", type(text_io))

    if not (DISCOVERY_COLLECTION_ID and DISCOVERY_ENVIRONMENT_ID):
        print("---> Skipping Discovery feed <--- (not configured)")
        return

    add_doc = discovery.add_document(
        environment_id=DISCOVERY_ENVIRONMENT_ID,
        collection_id=DISCOVERY_COLLECTION_ID,
        file=text_io, filename="testfile").get_result()

    print(json.dumps(add_doc, indent=2))
