
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

# Max crawl depth
max_depth = 1

# Create array to store URLs that we have already crawled
crawled_urls = []

# Initialize the Discovery client
#
load_dotenv()
DISCOVERY_COLLECTION_ID = os.environ.get('DISCOVERY_COLLECTION_ID')
DISCOVERY_ENVIRONMENT_ID = os.environ.get('DISCOVERY_ENVIRONMENT_ID')
discovery = DiscoveryV1(version='2020-12-08')


@app.route("/api/v1/crawlme", methods=['POST'])
@prometheus.track_requests
def crawlme():
    """crawlme url route"""
    input = request.get_json(force=True)
    print("INPUT:", input)
    # TODO: queue these and run with threading
    crawl_url(input.get('url'))

    state = {"status": "Accepted"}
    return jsonify(state), 202


def crawl_url(url, depth=0):
    
    print("url coming into crawl_url:", url)
    if "http" not in url:
        url = "https://" + url

    print("new url after supposedly adding https:", url)
    
    if url in crawled_urls:
        print("Skipping already crawled url:", url)
        return
    crawled_urls.append(url)

    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
        return

    soup = BeautifulSoup(page.content, 'lxml')
    send_to_discovery(soup.prettify(), url)

    if depth < max_depth:
        depth += 1
        # recursive crawl...
        # extract links from 'href' and 'src'
        # future: do something intelligent to only crawl interesting ones
        new_links = [
            item['href'] if item.get('href') is not None else item['src']
            for item in soup.select('[href^="http"], [src^="http"]')
        ]
        print('All URLs found: ', new_links)
        for i in new_links:
            crawl_url(i, depth)
        # for link in soup.find_all('a'):
        # print(link.get('href'))


def send_to_discovery(text_io, url):

    if not (DISCOVERY_COLLECTION_ID and DISCOVERY_ENVIRONMENT_ID):
        print("---> Skipping Discovery feed <--- (not configured)")
        return
    
    # use url domain-path as file name
    domain = urlparse(url).netloc
    path = urlparse(url).path.strip("/")
    url_as_string = str(domain + "-" + path)
#    output_file = os.path.join(url_as_string + suffix)

    add_doc = discovery.add_document(
        environment_id=DISCOVERY_ENVIRONMENT_ID,
        collection_id=DISCOVERY_COLLECTION_ID,
        file=text_io, filename=url_as_string).get_result()

    print(json.dumps(add_doc, indent=2))

    # write html to file as text, use url domain-path as file name
    # domain = urlparse(url).netloc


# def get_filename(url):
#
    # # !! Need to remove all '/' and replace with '-', below doesn't work
    # # path = urlparse(url).path.split.replace("/","-")
    # path = urlparse(url).path.strip("/")
    # url_as_string = str(domain + "-" + path)
    # suffix = '.txt'
    # save_path = os.getcwd()
    # output_file = os.path.join(save_path, url_as_string + suffix)
    # with open(output_file, 'w', encoding='utf-8') as file:
        # file.write(soup.prettify())
    # print('Output file name is ', output_file)
    # print("\n")
