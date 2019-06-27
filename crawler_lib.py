import requests
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/reddit-crawler/config.ini')

def send_message(title, title_link, text, keyword, in_place = "", user = "", flair = ""):
    response = requests.post(
        config.get('slack','webhook'), data=json.dumps({'attachments': [ { 'fallback': title + ": " + text, 'title': title, 'title_link': title_link, 'text': text, 'footer': "Matched keyword '" + keyword + "'" + in_place , "author_name": "/u/" + user + ("" if flair == "" else " [" + flair + "]"), "author_link": "https://www.reddit.com/user/" + user} ] }),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def keyword_match(text):
    lowercase_text = text.lower()
    keywords = open(config.get('reddit','keywords'),'r')
    for keyword in keywords.readlines():
        if keyword.rstrip() == "":
            continue
        if keyword.rstrip() in lowercase_text:
            print(keyword.rstrip() + " found in text")
            return keyword.rstrip()
    print("no keywords found")
    return False
