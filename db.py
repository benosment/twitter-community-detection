from pymongo import MongoClient

def connect_db():
  client = MongoClient()
  db = client.twitter_database
  return db

def connect_tweets_db():
  db = connect_db()
  return db.tweets

def insert_tweet(tweet):
  ''' 
      Tweet is expected to be in json format
  '''
  tweets = connect_tweets_db()
  tweets.insert(tweet)  

def filter_tweets():
  ''' 
      Remove all tweets that do not have a mention or RT
  '''
  tweets = connect_tweets_db()
  tweets.remove({'entities.user_mentions' : []}) # find tweets without a mention

def find_retweets():
  # find retweets tweets, also shows up as a user_mention
  tweets = connect_tweets_db()
  return tweets.find({'text' : {'$regex' : '^RT'}}) 

def get_tweets():
  # return all tweets, returns a cursor
  tweets = connect_tweets_db()
  return tweets.find()

def get_num_tweets():
  cursor = get_tweets()
  return cursor.count()

if __name__ == '__main__':
  filter_tweets()
  
