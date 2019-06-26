import praw
import prawcore
import requests
import pprint
import json
import time
from crawler_lib import send_message, keyword_match
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(user_agent=config.get('reddit','user_agent'),
                     client_id=config.get('reddit','client_id'), client_secret=config.get('reddit','client_secret'))

subreddit = reddit.subreddit(config.get('reddit','subreddit'))

while True:
    try:
        for submission in subreddit.stream.submissions():
            if time.time() - submission.created_utc > 300:
                print("Thread " + submission.id + " was posted more than 5 minutes ago, skipping")
                continue
            flair = submission.author_flair_text
            if flair is None:
                flair = ""
            if keyword_match(submission.title):
                print("Matched thread " + submission.id)
                send_message(submission.title, submission.url, submission.selftext, keyword_match(submission.title), ' in title', submission.author.name, flair)
                continue
            elif keyword_match(submission.selftext):
                print("Matched thread " + submission.id)
                send_message(submission.title, submission.url, submission.selftext, keyword_match(submission.selftext), ' in text', submission.author.name, flair)
                continue
            else:
                print("No keyword match on thread " + submission.id)
    except prawcore.exceptions.ResponseException:
        print("Got a bad response from reddit API, waiting 5 seconds before continuing")
        time.sleep(5)
    except prawcore.exceptions.RequestException:
        print("Unable to connect to reddit.com, likely a Reddit API outage")
        time.sleep(5)
