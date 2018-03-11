from TwitterSearch import *
import json
from time import sleep

import requests
def generate_hashtags(baselist):
    url= "http://d212rkvo8t62el.cloudfront.net/tag/"
    for base in baselist:
        one = baselist[base][0][1:]
        resp= requests.get(url=url+one)
        data= resp.json()
        tmp = baselist[base]
        baselist[base] = ['#'+hashtag['tag'] for hashtag in data['results']][:4]
        if len(baselist[base]) == 0:
            baselist[base] = tmp
    return baselist

def get_auth():
    global i
    global api
    ts = TwitterSearch(
        consumer_key=keys[i]['consumer_key'],
        consumer_secret=keys[i]['consumer_secret'],
        access_token=keys[i]['access_token'],
        access_token_secret=keys[i]['access_token_secret']
    )
    i += 1
    return ts


def limit_handled(keys, query, api, errors):

    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(query, or_operator=True)
        return [errors, api, api.search_tweets_iterable(tso)]
    except TwitterSearchException as e:
        if e.code == 429:
            print("API cooldown")
            errors += 1

            if errors == len(keys):
                print("MAX SHUTDOWN: Waiting 1 minute and retrying...")
                sleep(60)
                print("Retrying now!")

            print(errors)
            print(errors % len(keys))
            errors = errors % len(keys)
            api = get_auth()

        return [errors, api, None]


def compileHash(hashlist):
    return [" OR ".join(hashlist[x]) for x in hashlist.keys()]


if __name__ == "__main__":
    global api
    global keys
    global i

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
    i = 0
    api = get_auth()
    errors = 0
    # hashlist = generate_hashtags({'ChicagoBulls': ['#BullsNation'],
    #             'TorontoRaptors': ['#WeTheNorth'],
    #             'NBA': ['#NBA'], 'Blazers': ['#RipCity'], 'Detroit': ['#DetroitBasketball'],
    #             'Grizzlies': ['GrindCity'], 'Lakers': ['#LakeShow'], 'Sacramento': ['#SacramentoProud'],
    #             'Bucks': ['#OwnTheFuture'], 'Philadelphia': ['#MADEinPHILA'], 'GSWarriors': ['#DubNation'],
    #             'Charlotte': ['#BuzzCity'], 'DenverNuggets': ['#MileHighBasketball'], 'AtlantaHawks': ['#TrueToAtlanta'],
    #             'DallasMavericks': ['#MFFL'], 'PhoenixSuns': ['#WeArePHX'], 'LAClippers': ['#ItTakesEverything'],
    #             'MiamiHeats': ['#HEATisOn'], 'OrlandoMagic': ['#LetsGoMagic'], 'Celtics': ['#Celtics'],
    #             'Rockets': ['#Rockets50'], 'Pacers': ['#GoPacers'], 'Pelicans': ['#Pelicans'], 'Knicks': ['#Knicks'],
    #             'BrooklynNets': ['#BrooklynGrit'], 'UtahJazz': ['#TakeNote'], 'ClevelandCavaliers': ['#DefendTheLand'],
    #             'WashingtonWizards': ['#DCFamily']})

    hashlist = generate_hashtags({})

    hashkeys = list(hashlist.keys())

    stats_retr = 0

    for x in range(len(hashkeys)):
        file = hashkeys[x]
        with open("./data/NBA/" + file + ".json", "w+") as f:
            query_list = hashlist[file]
            print("Perform " + " OR ".join(query_list) + "(" + file + ")")
            raw_data = None
            while raw_data is None:
                [errors, api, raw_data] = limit_handled(keys, query_list, api, errors)

            data = [x for x in raw_data]
            print("Retrieved " + str(len(data)) + " tweets for " + file)
            json.dump(data, f)
