import datetime
import json
import os
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import jsonify
from flask import request
from ibm_watson import DiscoveryV1

from server import app
from server.routes import prometheus
from server.config import db
from urllib.parse import urlparse

# Max crawl depth
max_depth = 1

# Create array to store URLs that we have already crawled
crawled_urls = []

# Initialize the Discovery client
#
load_dotenv()
DISCOVERY_COLLECTION_ID = os.environ.get('DISCOVERY_COLLECTION_ID')
DISCOVERY_ENVIRONMENT_ID = os.environ.get('DISCOVERY_ENVIRONMENT_ID')

discovery = None
if DISCOVERY_COLLECTION_ID and DISCOVERY_ENVIRONMENT_ID:
    discovery = DiscoveryV1(version='2020-12-08')


@app.route("/api/v1/crawlme", methods=['POST'])
@prometheus.track_requests
def crawlme():
    print("I'm in the crawlme function!")
    """crawlme url route"""
    crawl_this = request.get_json(force=True)
    print("INPUT:", crawl_this)
    
    # Check if url=pause; workaround for Assistant pauses not working with SMS with Twilio integration
    if crawl_this.get('url')=='pause':
        print("Sleeping...")
        # Wait for 6 seconds
        time.sleep(6)
        print("Slept for 6 seconds")

    else:
        # TODO: queue these and run with threading
        crawl_url(crawl_this.get('url'), datetime.datetime.now(), depth=0)

    state = {"status": "Accepted"}
    return jsonify(state), 202


def crawl_url(url, posted, depth=0, root_url=None):
    print("url coming into crawl_url:", url)
    if "http" not in url:
        url = "https://" + url
        print("new url after adding https (if needed):", url)

    if ' ' in url:
        url = url.replace(' ', '')
#        url.translate(None,' ')
        print("new url after removing spaces:", url)
        
    
    root_url = root_url or url
    
    # if db.is_crawled(url):
    if url in crawled_urls:
        print("Skipping already crawled url:", url)
        return
    crawled_urls.append(url)

    # filter out urls that end in .png, .js, .css
    end_url = os.path.basename(url)
    print("url basename:", end_url)

    if end_url.endswith(('.png', '.js', '.css', '.jpg', '.aspx', '.php', '.jsp', '.php', '.rss', '.ashx', '.ece')):
        print('invalid url', end_url)
        return

    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
        return

    db.insert_crawl_me(
        {
            'URL': url,
            'PARENT_URL': root_url,
            'POSTED': posted,
            'DEPTH': depth,
            'CRAWLED': datetime.datetime.now(),
            'STATUS': page.status_code
        }
    )

    soup = BeautifulSoup(page.content, 'lxml')
    send_to_discovery(soup.prettify(), url)
    
    # Check for a client-side redirect URL
    redirect = soup.find('meta',attrs={'http-equiv':'refresh'})
    if redirect:
        wait,text=redirect["content"].split(";")
        if text.strip().lower().startswith("url="):
            redirect_url=text[4:]
            print('redirect_url = ', redirect_url)
            crawl_url(redirect_url, posted, depth, root_url) 

    if depth < max_depth:
        depth += 1
        # recursive crawl...
        # extract links from 'href' and 'src'
        # future: do something intelligent to only crawl interesting ones
        new_links = [
            item['href'] if item.get('href') is not None else item['src']
            for item in soup.select('[href^="http"], [src^="http"]')
        ]
        for x in new_links:
            modified_links = x.split('?')[0]
        print('All URLs found: ', modified_links)
        for i in modified_links:
            crawl_url(i, posted, depth, root_url)
        # for link in soup.find_all('a'):
        # print(link.get('href'))


def send_to_discovery(text_io, url):

    if not discovery:
        print("---> Skipping Discovery feed <--- (not configured)")
        return
    
    # use url domain-path as file name
    domain = urlparse(url).netloc
    path = urlparse(url).path.split("/")
    filename = str(domain)
    if path:
        for i in range(1, len(path)):
            filename = str(filename + "\/" + path[i])
    print('filename:', filename)

    #    output_file = os.path.join(url_as_string + suffix)

    add_doc = discovery.add_document(
        environment_id=DISCOVERY_ENVIRONMENT_ID,
        collection_id=DISCOVERY_COLLECTION_ID,
        file=text_io, filename=filename).get_result()

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
