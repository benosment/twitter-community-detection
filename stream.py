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
import db

tweet_count = 0

class RetweetStreamListener(tweepy.StreamListener):
  def on_status(self, status):
    print status

  def on_data(self, data):
      # handle the raw data
      if 'in_reply_to_status_id' in data:
        status = tweepy.Status.parse(self.api, json.loads(data))
        # still getting non-english tweets, stream.filter(lang=['en']) does not
        # work yet. TODO - try hooking in CLD (common lang. detector) from chromium
        #if (status.user.lang == 'en') and hasattr(status, 'retweeted_status'):
        #if hasattr(status, 'retweeted_status'):
        if (status.user.lang == 'en'):
          print "%s: %s" % (status.user.screen_name.encode('utf-8'), 
                            status.text.encode('utf-8'))
          global tweet_count
          tweet_count += 1
          if tweet_count % 100 == 0:
            print "Tweet count: ", tweet_count
          # is it better to have the DB connection as an attribute of this listener?
          db.insert_tweet(json.loads(data))

  def on_limit(self, track):
    logging.warning("Rate limited")
    time.sleep(3)

  def on_timeout(self):
    logging.warning("Timeout.")

  def on_error(self, status_code):
    logging.error("Status code: %s" % status_code)
    time.sleep(3)
    return True  # return True to keep the stream alive

def logger_init():
  # load logging config file
  logging.config.fileConfig('logging.conf')
  logging.getLogger('streamLogger').info("Init")


def main():
  auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
  auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
  listener = RetweetStreamListener()
  stream = tweepy.Stream(auth, listener)
  # filter stream by location, coordinates are for NYC
  stream.filter(locations=[-74,40,-73,41])

if __name__ == '__main__':
  # initialize the logger
  logger_init()

  try:
    main()
  except KeyboardInterrupt:
    sys.exit()
  except Exception,e:
    logging.getLogger('streamLogger').exception("Exception %s" % str(e))
    time.sleep(3)
