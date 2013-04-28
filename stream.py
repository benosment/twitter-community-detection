__author__ = 'bosment'

import tweepy
import time
import sys
import settings
import logging
import logging.config
import pdb
import json
from pymongo import MongoClient

class RetweetStreamListener(tweepy.StreamListener):
  def on_data(self, data):
      # handle the raw data
      if 'in_reply_to_status_id' in data:
        status = tweepy.Status.parse(self.api, json.loads(data))
        # TODO - still getting non-english tweets, try stream.filter(lang=['en'])
        if (status.user.lang == 'en') and hasattr(status, 'retweeted_status'):
          print "%s: %s" % (status.user.screen_name.encode('utf-8'), 
                            status.text.encode('utf-8'))
          # is it better to have the DB connection as an attribute of this listener?
          insert_tweet(json.loads(data))

  def on_limit(self, track):
    logging.warning("Rate limited")
    time.sleep(3)

  def on_timeout(self):
    logging.warning("Timeout.")

  def on_error(self, status_code):
    logging.error("Status code: %s" % status_code)
    time.sleep(3)
    return True  # return True to keep the stream alive


def connect_db():
  client = MongoClient()
  db = client.twitter_database
  return db

def insert_tweet(tweet):
  ''' 
      Tweet is expected to be in json format
  '''
  db = connect_db()
  tweets = db.tweets
  tweets.insert(tweet)  

def logger_init():
  # load logging config file
  logging.config.fileConfig('logging.conf')
  logging.getLogger('streamLogger').info("Init")

def main():
  auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
  auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
  db = connect_db()
  listener = RetweetStreamListener()
  stream = tweepy.Stream(auth, listener)
  stream.sample()
  #stream.retweet()
  #stream.filter(track=['boston'])

if __name__ == '__main__':
  # initialize the logger
  logger_init()

  try:
    main()
  except KeyboardInterrupt:
    sys.exit()
  except Exception,e:
    # TODO - what's the traceback here?
    logging.getLogger('streamLogger').exception("Exception %s" % str(e))
    time.sleep(3)
