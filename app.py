import os, sys
from flask import Flask
from flask_hookserver import Hooks
import tweepy

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

twitter_consumer_key = os.environ['OSII_BOT_CONSUMER_KEY']
twitter_consumer_secret = os.environ['OSII_BOT_CONSUMER_SECRET']
twitter_access_token = os.environ['OSII_BOT_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['OSII_BOT_ACCESS_TOKEN_SECRET']
github_webhooks_secret = os.environ['OSII_BOT_WEBHOOKS_SECRET']

# flask app
app = Flask(__name__)

# twitter auth by tweepy
twitter_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)

# github webhooks & request checking options
app.config['GITHUB_WEBHOOKS_KEY'] = github_webhooks_secret
app.config['VALIDATE_IP'] = False
app.config['VALIDATE_SIGNATURE'] = True
hooks = Hooks(app, url='/webhooks')

# flask routes
@app.route('/')
def hello():
    return '<a href="{0}">{0}</a>'.format('https://github.com/open-source-ideas')

@hooks.hook('issues')
def issues(data, delivery):
    twitter_update_status = 'This hook is not implemented'
    # Tweet only newly created issues
    if (data['action'] == 'opened'):
        tweet_max_len = 278
        title = 'New open source idea!'
        url = data['issue']['html_url']
        desc = data['issue']['title'][0:(tweet_max_len-len(title)-len(url))]
        tweet = '{} {} {}'.format(title, desc, url)
        twitter_update_status = twitter_api.update_status(tweet)
    return str(twitter_update_status)
    
# app running on c9.io
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
