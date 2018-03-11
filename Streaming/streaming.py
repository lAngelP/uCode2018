import tweepy
from time import time, sleep

class StreamData:
    def __init__(self, id_tweet, url, posted_at, username, displayname, text, fav, rt):
        self.id = id_tweet
        self.url = url
        self.posted_at = posted_at
        self.username = username
        self.displayname = displayname
        self.text = text
        self.fav = fav
        self.rt = rt

    def __str__(self):
        "Usuario: "+self.username+"\n"+ \
        "Posted_at"+self.posted_at+"\n"+ \
        "Url :"+self.url+"\n"+ \
        "Display: "+self.displayname

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()

    def on_status(self, status):
        global tfinal
        global myStream
        if status.text[0:2] != "RT":
            print("Received Tweet")
            with open("../website/data/test.txt", "w") as f:
                f.write(str(status.user.screen_name)+","+str(status.id))
            
        else:
            print("Received Retweet")
        #print(time()-tfinal)
        if time()>tfinal:
            myStream.disconnect()

    def on_error(self, status_code):
        print("Error ", status_code)
        data = None
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def get_auth(i, keys):
    auth = tweepy.OAuthHandler(keys[i]['consumer_key'], keys[i]['consumer_secret'])
    auth.set_access_token(keys[i]['access_token'], keys[i]['access_token_secret'])
    return [i + 1, tweepy.API(auth)]


def start_streaming(hashtag, nombre, equipos, fecha, lugar, tinicio, duracion):
    global tfinal
    global myStream
    insertar_evento()
    print("esperando "+ str(tinicio-time())+" segundos")
    #Esperar tiempo de inicio
    sleep(tinicio-time())
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

    i = 1
    print("Comenzando")
    tfinal = tinicio+duracion
    while time()<tinicio+duracion:
        [i, api] = get_auth(i, keys)
        myStreamListener = MyStreamListener()

        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=[hashtag])
        print(tinicio+duracion-time())
