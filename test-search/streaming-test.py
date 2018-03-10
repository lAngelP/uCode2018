import tweepy


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def MyStreamListener(self):
        self.x = 0

    def on_status(self, status):
        print(dir(status))
        print("Dir: ", dir(status.user))
        print("URL ", status.user.profile_image_url)
        print("Posted: ", status.created_at)
        print("Username: ", status.user.screen_name)
        print("Display: ", status.user.name)
        print("Text: ", status.text)
        print("FAV: ", status.favorite_count)
        print("RT: ", status.retweet_count)

        if status.text[0:2] == "RT":
            print("Is RT")
        else:
            print("Not a RT")

    def on_error(self, status_code):
        print("Error ", status_code)
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


if __name__ == "__main__":
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

    auth = tweepy.OAuthHandler(keys[1]['consumer_key'], keys[1]['consumer_secret'])
    auth.set_access_token(keys[1]['access_token'], keys[1]['access_token_secret'])

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=['python'])
