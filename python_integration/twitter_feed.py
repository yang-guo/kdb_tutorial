import numpy as np
import json
from datetime import datetime
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from qpython import qconnection



class Listener(StreamListener):
    def __init__(self, host, port, username = '', password = ''):
        self.qconn = qconnection.QConnection(host = host, port = port, username = username, password = password)
        self.qconn.open()

        super(self.__class__, self).__init__()

    def on_data(self, data):
        tweet = json.loads(data)
        text = tweet['text'].encode('ascii', 'ignore')
        user = tweet['user']['screen_name'].encode('ascii', 'ignore')

        self.qconn.async('.u.upd', np.string_('tweets'), [
            self._get_current_time(),
            np.string_(user),
            text,
            data.encode('ascii', 'ignore')
        ])
        return True
    
    def on_error(self, status):
        print status

    def _get_today(self):
        return np.datetime64(datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))

    def _get_current_time(self):
        return np.timedelta64((np.datetime64(datetime.utcnow()) - self._get_today()), 'ns')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise Exception('need three arguments')
    auth_file = sys.argv[1]
    keywords = sys.argv[2]
    tp_port = int(sys.argv[3])

    try:
        twitter_secret_dict = dict(x.split('=') for x in open(auth_file).read().strip().split('\n'))	
        consumer_key = twitter_secret_dict['CONSUMER_KEY']
        consumer_secret = twitter_secret_dict['CONSUMER_SECRET']
        access_token = twitter_secret_dict['ACCESS_TOKEN']
        access_token_secret = twitter_secret_dict['ACCESS_SECRET']
    except Exception, err:
        raise Exception('auth file is invalid')

    listener = Listener(host = 'localhost', port = tp_port)
    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track = keywords.split(","))
