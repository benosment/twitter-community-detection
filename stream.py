__author__ = 'bosment'

import tweepy
import time
import sys
import settings

def log_error(msg):
    timestamp = time.strftime('%a %b %d %Y %H:%M:%S')
    sys.stderr.write("%s - %s\n" % (timestamp,msg))


class RetweetStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # TODO - still getting non-english tweets, try stream.filter(lang=['en'])
        if (status.user.lang == 'en') and hasattr(status, 'retweeted_status'):
            print "%s: %s" % (status.user.screen_name.encode('utf-8'), status.text.encode('utf-8'))
    def on_limit(self, track):
        log_error("Rate limited")
        time.sleep(3)

    def on_timeout(self):
        log_error("Timeout.")

    def on_error(self, status_code):
        log_error("Status code: %s" % status_code)
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

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception,e:
        log_error("Exception: %s" % str(e))
        time.sleep(3)



