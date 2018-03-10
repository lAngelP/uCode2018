from TwitterSearch import *
import json

tso = TwitterSearchOrder()
ts = TwitterSearch(
                consumer_key = 'nRg8SIso25KTnYE0Yn1tec2zb',
                consumer_secret = 's26emswOPnExmaYjhgRUwKzRo84HnISBWJbCm4zUPbAnDJoIzZ',
                access_token = '2510636970-HjkdkkXeT7syJ0pZ9xPbr3kILTF3sUaq7l5JU4I',
                access_token_secret = 'kQCjoa2xkFe5VqY8e0ryjqV2ds1tyXpop1eEDXJvfUH3r'
            )
hashlist = {'RealMadrid':['#HalaMadrid', '#Realmadrid'], 'Juventus':['#ForzaJuve'], 
            'BayernMunich': ['#FCBayern'], 'ChicagoBulls': ['#BullsNation', '#Bulls'],
            'TorontoRaptors': ['#TeamToronto', '#RTZ']}
            
for hashtag in hashlist:
    lista = hashlist[hashtag]
    with open(hashtag+'.json', 'w') as outfile:
        try:
            tso.set_keywords(lista)
            number_tweets = 0
            for tweet in ts.search_tweets_iterable(tso):
                if number_tweets > 1:
                    break
                else:
                    number_tweets += 1
                    json.dump(tweet, outfile)

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)