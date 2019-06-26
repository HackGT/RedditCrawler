# Reddit Crawler
ZOMG THE INTERNET IS DOWN, or at least Reddit seems to think so. These scripts will continuously crawl comments and threads on /r/gatech for pre-defined keywords. If a match is found, a Slack message is sent with the relevant comment or thread.

## Configuration
_Note:_ You need Python 2.7 for this. It's not written to support 3 (yet).

 1. Clone the repository to a location of your choosing.
	 - `git clone https://github.gatech.edu/ResNet/RedditCrawler.git`
 2. Install dependencies.
	 - `pip install -r requirements.txt`
 3. Copy `config.example.ini` to `config.ini`
 4. Get Reddit API credentials
     - Go [here](https://www.reddit.com/prefs/apps/) and click "are you a developer? create an app..." at the bottom of the page.
     - Fill out the form as follows:
	     - **Name:** Reddit Crawler (or whatever)
	     - **Type:** Script
	     - **Description:** Crawler for Slack notifications
	     - **About URL:** _Leave blank_
	     - **Redirect URL:** `http://localhost:8080`
     - On the next page you'll be provided with credentials.
	     - **Client ID:** 14-character string under _personal use script_
	     - **Client Secret:** 27-character string labeled _secret_
5. Get a Slack Webhook
	- Go to `https://my.slack.com/apps` and search for _webhook_.
	- Click _Incoming Webhook_ then _Add Configuration_.
	- Select what channel the hook will send messages to, then click _Save_.
	- You'll see a **Webhook URL** displayed. Save this for use later.
	- Feel free to customize the name, icon, and other elements as you see fit.
6. Set keywords in `keywords.txt` as desired - one per line.
7. Edit `config.ini` as follows:
	- **user_agent:** Replace the username in the user agent as you see fit
	- **client_id:** From the Reddit app page in Step 4
	- **client_secret:** From the Reddit app page in Step 4
	- **keywords:** The name of your file with keywords, ex `keywords.txt`
	- **webhook:** The full URL from Slack in Step 5

## Running
You can run the scripts manually, ex. `python comments.py` or `python threads.py`, but a better option would be to use something like [supervisord](http://supervisord.org) to continuously run them in the background and handle any failures that come up. Configuring supervisor is outside of the scope of this document, though because we're nice people here's a sample config entry.

    [program:threads]
    command=python /var/www/RedditCrawler/production/threads.py
    directory=/var/www/RedditCrawler/production/
    redirect_stderr=true
    stdout_logfile=/var/www/RedditCrawler/production/supervisor.log
    user=nginx
    
    [program:comments]
    command=python /var/www/RedditCrawler/production/comments.py
    directory=/var/www/RedditCrawler/production/
    redirect_stderr=true
    stdout_logfile=/var/www/RedditCrawler/production/supervisor.log
    user=nginx
