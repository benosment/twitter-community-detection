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

def filter_tweets():
  ''' 
      Remove all tweets that do not have a mention or RT
  '''
  db = connect_db()
  tweets = db.tweets
  tweets.remove({'entities.user_mentions' : []}) # find tweets without a mention

def find_retweets():
  # find retweets tweets, also shows up as a user_mention
  tweets.find({'text' : {'$regex' : '^RT'}}) 
