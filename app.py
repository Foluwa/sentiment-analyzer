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
import tweepy
import csv 
from collections import Counter

import datetime
now = datetime.datetime.now()
prefix = now.strftime("%Y-%m-%d-%H:%M:%S")

from twitter_scrapper.twitter_scrapper import TwitterStreamListner 
tsl = TwitterStreamListner()



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


@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)
    return graphJSON

@app.route('/textblob/api',  methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        message = request.form['message']
        neu, neg, pos = tsl.ConvertTweetToCSV(message)
        print('NEU  ', neu, neg,pos)
    else:
        return render_template('page.html')
    return  jsonify({'negative':neg, 'neutral':neu, 'positive':pos})



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



if __name__ == '__main__':
    app.run()
