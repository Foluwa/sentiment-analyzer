from flask import Flask, jsonify, render_template,request,flash, redirect
import plotly
# import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px

import plotly.offline as py
from plotly.graph_objs import Pie, Layout,Figure

from textblob import TextBlob
import pandas as pd
import numpy as np
import json
#  Get tweets from twitter and save to csv
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
        print('this is me',search_query)
        def __init__(self, message):
            self.message = message
            print('foluwa ',search_query)
        # Open/create a file to append data to
        csvFile = open('{search_query}.csv'.format(search_query=search_query), 'a')
        #Use csv writer
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["USERID", "USERNAME", "USERFOLLOWERS", "TEXT", "CREATED", "ENCODE"])

        for tweet in tweepy.Cursor(api.search,
                                q = ['{search_query}'.format(search_query=search_query)],
                                since = "2020-02-02",
                                until = "2020-02-26",
                                lang = "en").items():
            # Write a row to the CSV file. I use encode UTF-8
            csvWriter.writerow([tweet.id,tweet.user.screen_name,tweet.user.followers_count,tweet.text, tweet.created_at, tweet.text.encode('utf-8')])
            print (tweet.created_at, tweet.text)
        csvFile.close()

        
app = Flask(__name__)

    # elif feature == 'Chart': 
    #     df = px.data.tips()
    #     fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu)
    #     fig.show()

@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    return render_template('main.html', plot=bar)

# @app.route('/search/<string:search_query>', methods=['GET', 'POST'])
# def search(search_query):
#     # Get Form Fields
#     feature = 'Bar'
#     bar = create_plot(feature)
#     print(search_query)

#     return render_template('main.html', plot=bar)
    

def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)+10
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'], # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    elif feature == 'Chart': 
        N = 4

        trace0 = go.Bar(
            x = np.linspace(0, 1, N),
            y = np.random.randn(N)+11
        )
        trace1 = go.Bar(
            x = np.linspace(0, 1, N),
            y = np.random.randn(N)+10
        )
        data = [trace0, trace1]
    else:
        N = 50
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)
    return graphJSON


@app.route('/api/<message>')
def sentiment(message):
        tsl = TwitterStreamListner()
        tsl.ConvertTweetToCSV(message)
        
        # text = TextBlob(message)
        # response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity}
        # print(response)
        return 'hello' #jsonify(response)




if __name__ == '__main__':
    app.run()
