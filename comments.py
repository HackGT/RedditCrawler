import praw
import prawcore
import requests
import pprint
import json
import time
from crawler_lib import send_message, keyword_match
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/reddit-crawler/config.ini')

reddit = praw.Reddit(user_agent=config.get('reddit','user_agent'),
                     client_id=config.get('reddit','client_id'), client_secret=config.get('reddit','client_secret'))

subreddit = reddit.subreddit(config.get('reddit','subreddit'))

while True:
    try:
        for comment in subreddit.stream.comments():
            if time.time() - comment.created_utc > 300:
                print("Comment " + comment.id + " was posted more than 5 minutes ago, skipping")
                continue
            flair = comment.author_flair_text
            if flair is None:
                flair = ""
            if keyword_match(comment.body):
                print("Matched comment " + comment.id)
                send_message("New reply to " + comment.link_title, "https://www.reddit.com" + comment.permalink, comment.body, keyword_match(comment.body), "", comment.author.name, flair)
            else:
                print("No keyword match on comment " + comment.id)
    except prawcore.exceptions.ResponseException as e:
        print("Got a bad response from reddit API, waiting 5 seconds before continuing")
        time.sleep(5)
    except prawcore.exceptions.RequestException:
        print("Unable to connect to reddit.com, likely a Reddit API outage")
        time.sleep(5)
