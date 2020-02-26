

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import csv 

#Variables that contains the user credentials to access Twitter API 
access_token = "465633653-x7NHimVAVuMGieuVi9GIRFL8TcuCFUxSQ4NjIdHR"
access_token_secret = "hSwFbdEv906tsZ67igSuKXrR8kh3yg1CDg2ElVo9ZO7dK"
consumer_key = "VoPZQmgqLLn9fO3TdSVgdza6q"
consumer_secret = "F1HEnesPeHSn514KYJNRbBFQumbRmrCf74IPsEKXJhIttj3aMT"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #[tweet.id,tweet.user.screen_name,tweet.user.followers_count,tweet.text, tweet.created_at, tweet.text.encode('utf-8')]
        print(data)
            
    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'webcoupers'
    stream.filter(track=['Lagos','Webcoupers'])