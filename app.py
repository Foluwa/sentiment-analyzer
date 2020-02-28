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

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/textblob/api',  methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        message = request.form['message']
        neutral, negative, positive = tsl.ConvertTweetToCSV(message)
        print(neutral, negative, positive)
    else:
        return render_template('page.html')
    return  jsonify({'negative':negative, 'neutral':neutral, 'positive':positive})


if __name__ == '__main__':
    app.run()
