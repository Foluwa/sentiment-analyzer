from flask import Flask, jsonify, render_template,request,flash, redirect
#  Get tweets from twitter and save to csv
import tweepy
import csv 
from textblob import TextBlob
import pandas as pd
import numpy as np
import json
import tweepy
import csv 

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

        def __init__(self, message):
            self.message = message

        # Open/create a file to append data to
        csvFile = open('{search_query}.csv'.format(search_query=search_query), 'a')
        #Using python csv writer
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["USERID", "USERNAME", "USERFOLLOWERS", "TEXT", "CREATED", "POLARITY", "SUBJECTIVITY", "SENTIMENT","ENCODE"])

        for tweet in tweepy.Cursor(api.search,q = ['{search_query}'.format(search_query=search_query)], since = "2020-02-02",until = "2020-02-26",lang = "en").items():

            print (tweet.created_at, tweet.text)
            tweet_details= TextBlob(tweet.text)
            print('The POLARITY IS ',tweet_details.polarity, 'and THE SUBJECTIVITY IS ', tweet_details.subjectivity)

            # https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
            # Subjective sentences generally refer to personal opinion, emotion or judgment
            # Objective refers to factual information. 
            if (tweet_details.polarity >= 0.3):
                sentiment='POSITIVE'
            elif (tweet_details.polarity >= 0.1):
                sentiment='NEUTRAL'
            else:
                sentiment='NEGATIVE'
            # Write a row to the CSV file. I use encode UTF-8
            csvWriter.writerow([tweet.id, tweet.user.screen_name, tweet.user.followers_count, tweet.text, tweet.created_at, 
                                tweet_details.polarity, tweet_details.subjectivity, sentiment ,tweet.text.encode('utf-8')])
        csvFile.close()

        search_query_csv= '{search_query}.csv'.format(search_query=search_query)
        print('The search query', search_query_csv)

        #DEALING WITH THE CSV
        data = pd.read_csv(search_query_csv)
        print(data.count())
        print('Result-----',data[data == 'POSITIVE'].count())
        print('______________________********______________________')
        #data.SENTIMENT.str.split(expand=True).stack().value_counts()

        arr_data = data.to_numpy()
        print('ARR DATA IS ',arr_data[0][7])

        return render_template('main.html')




        # if feature == 'Bar':
        #     N = 40
        #     x = np.linspace(0, 1, N)
        #     y = np.random.randn(N)+10
        #     df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        #     data = [
        #         go.Bar(
        #             x=df['x'], # assign x as the dataframe column 'x'
        #             y=df['y']
        #         )
        #     ]