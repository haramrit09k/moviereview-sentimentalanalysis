from flask import Flask, render_template, request
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from local_config import *
import pdb
import json
from collections import Counter
import sqlite3
import random
import string
import pickle

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="Ramu")

# Open classifier with pretrained dataset
open_classifier = open("naivebayes.pickle", "rb")
classifier = pickle.load(open_classifier)
open_classifier.close()

# Function to remove stopwords like "is", "was", etc...
def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words('english')]
    my_dict = dict([(word, True) for word in useful_words]) # We do this because Naive Bayes Classifier takes input in this format i.e (word, True)
    return my_dict

# Fetching Tweets from Twitter
auth = tweepy.OAuthHandler(cons_tok, cons_sec)
auth.set_access_token(app_tok, app_sec)
api = tweepy.API(auth)
# search_results = api.search(q="Samsung Galaxy S9 review", lang="en", count=100)
# Need to make the query keyword dynamic


@app.route('/', methods=['POST'])
def my_form_post():
    movienameinput = request.form['moviename']
    search_results = api.search(q = movienameinput, lang = "en", count = 100)
    tweet_text = []

    # Appending tweet text to an array
    for result in search_results:
        if 'RT @' not in result.text and not result.retweeted:
            result_text = result.text
            result_text = result_text.replace("-", " ")
            tweet_text.append(result_text)
            # print(result_text)
    vote_array = []

    for tweet in tweet_text:
        translator = str.maketrans('', '', string.punctuation) # Remove punctuations
        tweet = tweet.translate(translator)
        w = word_tokenize(tweet) # Tokenize the tweet i.e. convert words into parsable tokens
        w = create_word_features(w) 
        review = classifier.classify(w)
        if (review == 'positive'):
            vote_array.append(1)
        else:
            vote_array.append(0)

    no_of_ones = vote_array.count(1)
    # no_of_zeros = vote_array.count(0)
    
    positive_review_percentage = (no_of_ones/(len(vote_array)))*100
    
    review_result = "\n\n\nThe review is "+str(positive_review_percentage)+"% positive"        
    return render_template("index.html", review_result = review_result)



if __name__ == "__main__":
    app.run(debug=True)
