from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Guttenberg', 'Doktorarbeit']) # let's define all words we would like to have a look for
    tso.set_language('de') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'nRg8SIso25KTnYE0Yn1tec2zb',
        consumer_secret = 's26emswOPnExmaYjhgRUwKzRo84HnISBWJbCm4zUPbAnDJoIzZ',
        access_token = '2510636970-HjkdkkXeT7syJ0pZ9xPbr3kILTF3sUaq7l5JU4I',
        access_token_secret = 'kQCjoa2xkFe5VqY8e0ryjqV2ds1tyXpop1eEDXJvfUH3r'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)