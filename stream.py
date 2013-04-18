__author__ = 'bosment'

import tweepy
import time
import sys
import settings
import logging
import logging.config


class RetweetStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # TODO - still getting non-english tweets, try stream.filter(lang=['en'])
        if (status.user.lang == 'en') and hasattr(status, 'retweeted_status'):
            print "%s: %s" % (status.user.screen_name.encode('utf-8'), status.text.encode('utf-8'))
    def on_limit(self, track):
        logging.warning("Rate limited")
        time.sleep(3)

    def on_timeout(self):
        logging.warning("Timeout.")

    def on_error(self, status_code):
        logging.error("Status code: %s" % status_code)
        time.sleep(3)
        return True  # return True to keep the stream alive


def main():
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    listener = RetweetStreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.sample()
    #stream.retweet()
    #stream.filter(track=['boston'])

def logger_init():
    # load logging config file
    logging.config.fileConfig('logging.conf')

    # create logger
    logger = logging.getLogger('streamLogger')

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # return logger?
    # TODO - write to file? 


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



