#http://adilmoujahid.com/posts/2014/07/twitter-analytics/


from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

keys = [{"consumer_key": 'nRg8SIso25KTnYE0Yn1tec2zb',  # Jorpilo
             "consumer_secret": 's26emswOPnExmaYjhgRUwKzRo84HnISBWJbCm4zUPbAnDJoIzZ',
             "access_token": '2510636970-HjkdkkXeT7syJ0pZ9xPbr3kILTF3sUaq7l5JU4I',
             "access_token_secret": 'kQCjoa2xkFe5VqY8e0ryjqV2ds1tyXpop1eEDXJvfUH3r'},

            {"consumer_key": 'bjQ8FIJmBc0cH6sIzHEJBZfTB',  # lAngelP 1
             "consumer_secret": '59fdyTZu8j12IPb3hQvabyu9pe1dqtBlLaD2S1yBkHjCFXgZYw',
             "access_token": '2274344732-eWTEjJO9eZQ2rzpWr9HeIWXflv2v2tKbgTcovk2',
             "access_token_secret": 'XMxK5l0nz2Yjhv2XWH16eyfXhjfcZx3nUKp84cxbfZxV2'},

            {"consumer_key": '9M0kDfuRrz693qARlVL29CMBv',  # Giorgi
             "consumer_secret": 'hzECvDbxin5YA4GCISRLTwwAfGDtzPtTNfY3nbl6ibeFqTelsu',
             "access_token": '868335170-gcttYgeFnQsklJaI7FC1uhvk78G9o9ha4gIcElSx',
             "access_token_secret": '4qfXmFZhlyYFDzpwIHBstTRpVt7O7hBPI2jUCjTnLc9M8'}]

class listener(StreamListener):

    def on_status(self, status):
        print(status.retweet)
        print('------')

    def on_error(self, status):
        print(status)
        print('Hola')

if __name__ == '__main__':
    auth = OAuthHandler(keys[2]['consumer_key'], keys[2]['consumer_secret'])
    auth.set_access_token(keys[2]['access_token'], keys[2]['access_token_secret'])

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["car"])