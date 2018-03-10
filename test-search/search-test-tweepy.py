from TwitterSearch import *
import json

import requests
def generate_hashtags(baselist):
    url= "http://d212rkvo8t62el.cloudfront.net/tag/"
    for base in baselist:
        one = baselist[base][1:]
        resp= requests.get(url=url+one)
        data= resp.json()
        baselist[base] = ['#'+hashtag['tag'] for hashtag in data['results']][:4]
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


def limit_handled(query):
    global errors
    global api

    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(query, or_operator=True)
        errors = 0
        return api.search_tweets_iterable(tso)
    except TwitterSearchException as e:
        if e.code == 429:
            print("API cooldown")
            errors += 1
            api = get_auth()

            if errors == len(keys):
                print("MAX SHUTDOWN: Waiting 1 minute and retrying...")
                sleep(60)

        return None


def compileHash(hashlist):
    return [" OR ".join(hashlist[x]) for x in hashlist.keys()]


if __name__ == "__main__":

    keys = [{"consumer_key": 'nRg8SIso25KTnYE0Yn1tec2zb',  # Jorpilo
             "consumer_secret": 's26emswOPnExmaYjhgRUwKzRo84HnISBWJbCm4zUPbAnDJoIzZ',
             "access_token": '2510636970-HjkdkkXeT7syJ0pZ9xPbr3kILTF3sUaq7l5JU4I',
             "access_token_secret": 'kQCjoa2xkFe5VqY8e0ryjqV2ds1tyXpop1eEDXJvfUH3r'},

            {"consumer_key": 'bjQ8FIJmBc0cH6sIzHEJBZfTB',  # lAngelP 1
             "consumer_secret": '59fdyTZu8j12IPb3hQvabyu9pe1dqtBlLaD2S1yBkHjCFXgZYw',
             "access_token": '2274344732-eWTEjJO9eZQ2rzpWr9HeIWXflv2v2tKbgTcovk2',
             "access_token_secret": 'XMxK5l0nz2Yjhv2XWH16eyfXhjfcZx3nUKp84cxbfZxV2'}]
    i = 0
    api = get_auth()
    errors = 0
    hashlist = generate_hashtags({'RealMadrid': ['#HalaMadrid'], 'Juventus': ['#ForzaJuve'],
                'BayernMunich': ['#FCBayern'], 'ChicagoBulls': ['#BullsNation'],
                'TorontoRaptors': ['#TeamToronto', '#RTZ']})
    hashkeys = list(hashlist.keys())

    stats_retr = 0

    while True:
        for x in range(len(hashkeys)):
            file = hashkeys[x]
            h = hash[x]
            with open("./data/" + file + ".json", "w") as f:
                query_list = hashlist[file]
                print("Perform " + " OR ".join(query_list))
                raw_data = None
                while raw_data is None:
                    raw_data = limit_handled(query_list)

                data = [x for x in raw_data]
                print("Retrieved " + str(len(data)) + " tweets for " + file)
                json.dump(data, f)