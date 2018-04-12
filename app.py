import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from local_config import *
import pdb
import json
from collections import Counter
import sqlite3

db = "twit_data.db"

class twitter_listener(StreamListener):

	def __init__(self, num_of_tweets_to_grab, stats, get_tweet_html, retweet_count=100):
		self.counter = 0
		self.num_of_tweets_to_grab = num_of_tweets_to_grab
		self.retweet_count = retweet_count
		self.stats = stats
		self.get_tweet_html = get_tweet_html

	def on_data(self, data):
		try:
			json_data = json.loads(data)
			self.counter += 1
			retweet_count = json_data["retweeted_status"]["retweet_count"]
			
			if retweet_count >= self.retweet_count:
				print(json_data["text"])
				self.stats.add_top_tweets(self.get_tweet_html(json_data["id"]))
			
			if self.counter >= self.num_of_tweets_to_grab:
				return False

			return True

		except:
			pass

	def on_error(self, status):
		print(status)

class TwitterMain():
	def __init__(self, num_of_tweets_to_grab, retweet_count, conn):
		self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
		self.auth.set_access_token(app_tok, app_sec)

		self.api = tweepy.API(self.auth)
		self.num_of_tweets_to_grab = num_of_tweets_to_grab
		self.retweet_count = retweet_count
		self.stats = stats()
		self.conn = conn
		self.c = self.conn.cursor()

	def get_streaming_data(self):
		twitter_stream = Stream(self.auth, twitter_listener(num_of_tweets_to_grab=self.num_of_tweets_to_grab,retweet_count=self.retweet_count, stats = self.stats, get_tweet_html=self.get_tweet_html))
		# twitter_stream.filter(track = ['python'])
		try:
			twitter_stream.sample()
		except Exception as e:
			print(e.__doc__)

		top_tweets = self.stats.get_stats()
		print(len(top_tweets))


		for t in top_tweets:
			self.c.execute("INSERT INTO twit_data VALUES (?, DATETIME('now'))", (t,))

		self.conn.commit()

	def get_tweet_html(self, id):
		oembed = self.api.get_oembed(id=id, hide_media=True, hide_thread = True)

		tweet_html = oembed['html'].strip("\n")

		return tweet_html

class stats():

	def __init__(self):
		self.top_tweets = []

	def add_top_tweets(self, tweet_html):
		self.top_tweets.append(tweet_html)

	def get_stats(self):
		return self.top_tweets

if __name__ == "__main__":
	num_of_tweets_to_grab = 1000
	retweet_count = 1000
	try:
		conn = sqlite3.connect(db)
		twit = TwitterMain(num_of_tweets_to_grab, retweet_count, conn)
		twit.get_streaming_data()



	except Exception as e:
		print(e.__doc__)

	finally:
		conn.close()	
