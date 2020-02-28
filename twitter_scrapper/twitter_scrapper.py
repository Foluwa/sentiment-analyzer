from flask import Flask, jsonify, render_template, request, flash, redirect, Response
import tweepy
import csv 
from textblob import TextBlob
import pandas as pd
import numpy as np
import json
import tweepy
import csv 

import plotly.graph_objects as go
import datetime
now = datetime.datetime.now()
prefix = now.strftime("%Y-%m-%d-%H:%M:%S")


ACCESS_TOKEN = "465633653-x7NHimVAVuMGieuVi9GIRFL8TcuCFUxSQ4NjIdHR"
ACCESS_TOKEN_SECRET = "hSwFbdEv906tsZ67igSuKXrR8kh3yg1CDg2ElVo9ZO7dK"
CONSUMER_KEY = "VoPZQmgqLLn9fO3TdSVgdza6q"
CONSUMER_SECRET = "F1HEnesPeHSn514KYJNRbBFQumbRmrCf74IPsEKXJhIttj3aMT"


auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class TwitterStreamListner():
    
# Method to open a file and append data to that specific file
    # print(message)
    def ConvertTweetToCSV(self,message):
        search_query = message
        sentiment_list = []
        self.message = message
        self.sentiment_list = sentiment_list
        type(self.sentiment_list)

        #Using python csv writer
        csvFile = open('{search_query}.csv'.format(search_query=search_query), 'a')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["USERID", "USERNAME", "USERFOLLOWERS", "TEXT", "CREATED", "POLARITY", "SUBJECTIVITY", "SENTIMENT"])

        for tweet in tweepy.Cursor(api.search,q = ['{search_query}'.format(search_query=search_query)], since = "2020-02-20",until = "2020-02-28",lang = "en").items():

            print (tweet.created_at, tweet.text)
            tweet_details= TextBlob(tweet.text)
            print('The POLARITY IS ',tweet_details.polarity, 'and THE SUBJECTIVITY IS ', tweet_details.subjectivity)

            # https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
            # Subjective sentences generally refer to personal opinion, emotion or judgment
            # Objective refers to factual information. 

            if (tweet_details.polarity >= 0.2):
                sentiment='POSITIVE'
            elif (tweet_details.polarity == 0):
                sentiment='NEUTRAL'
            else:
                sentiment='NEGATIVE'
            # Write a row to the CSV file.
            csvWriter.writerow([tweet.id, tweet.user.screen_name, tweet.user.followers_count, tweet.text, tweet.created_at,tweet_details.polarity, tweet_details.subjectivity, sentiment])
        csvFile.close()

        search_query_csv_file= '{search_query}.csv'.format(search_query=search_query)
        print('The search query', search_query_csv_file)

        #DEALING WITH THE CSV
        df = pd.read_csv(search_query_csv_file)
        sentiment_list = df['SENTIMENT'].value_counts()
        print(sentiment_list)

        #TODO: Handle exception for when there are no values for negative or positive or neutral as in case for 'zeezahdevs' query 
        negative  = sentiment_list.NEGATIVE
        neutral = sentiment_list.NEUTRAL 
        positive = sentiment_list.POSITIVE  
        negative  = int(negative)
        neutral = int(neutral)
        positive = int(positive) 
        return neutral, negative, positive
