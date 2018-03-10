from __future__ import unicode_literals
import tweepy
import json

def getAuth():
  global i
  global api
  auth = tweepy.OAuthHandler(keys[i]['consumer_key'], keys[i]['consumer_secret'])
  auth.set_access_token(keys[i]['access_token'], keys[i]['access_token_secret'])
  i += 1
  return tweepy.API(auth)


def limit_handled(cursor):
  try:
      yield cursor.next()
      errors = 0
  except tweepy.RateLimitError:
      print("API cooldown")
      errors += 1
      api = getAuth()
      
      if(errors == len(keys)):
        print("MAX SHUTDOWN: Waiting 1 minute and retrying...")
        sleep(60)
      
      return None

def compileHash(hashlist):
  return [ " OR ".join(hashlist[x]) for x in hashlist.keys()]

if __name__ == "__main__":

    keys = [{"consumer_key": 'nRg8SIso25KTnYE0Yn1tec2zb', #Jorpilo
    "consumer_secret": 's26emswOPnExmaYjhgRUwKzRo84HnISBWJbCm4zUPbAnDJoIzZ',
    "access_token": '2510636970-HjkdkkXeT7syJ0pZ9xPbr3kILTF3sUaq7l5JU4I',
    "access_token_secret": 'kQCjoa2xkFe5VqY8e0ryjqV2ds1tyXpop1eEDXJvfUH3r'},

    {"consumer_key": 'bjQ8FIJmBc0cH6sIzHEJBZfTB', #lAngelP 1
    "consumer_secret": '59fdyTZu8j12IPb3hQvabyu9pe1dqtBlLaD2S1yBkHjCFXgZYw',
    "access_token": '2274344732-eWTEjJO9eZQ2rzpWr9HeIWXflv2v2tKbgTcovk2',
    "access_token_secret": 'XMxK5l0nz2Yjhv2XWH16eyfXhjfcZx3nUKp84cxbfZxV2'}]
    i = 0
    api = getAuth()
    errors = 0
    hashlist = {'RealMadrid':['#HalaMadrid', '#Realmadrid'], 'Juventus':['#ForzaJuve'],
        'BayernMunich': ['#FCBayern'], 'ChicagoBulls': ['#BullsNation', '#Bulls'],
        'TorontoRaptors': ['#TeamToronto', '#RTZ']}
    hashkeys = list(hashlist.keys())
    hash = compileHash(hashlist)

    stats_retr = 0

    while True:
      for x in range(len(hash)):
        file = hashkeys[x]
        h = hash[x]
        with open("./data/" + file + ".json", "w") as f:
          print(h)
          h = "#HalaMadrid"
          cursor = tweepy.Cursor(api.search, q=h, rpp = 100, count = 100)
          data = limit_handled(cursor.items())
          data_list = [one._json for one in data]
          print("Retrieved " + str(len(data_list)) + " tweets for " + file)
          json.dump(data_list, f)

