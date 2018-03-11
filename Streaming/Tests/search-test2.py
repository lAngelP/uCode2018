from TwitterSearch import TwitterUserOrder, TwitterSearchException

try:
    tuo = TwitterUserOrder("some_user")
    tuo.set_trim_user(True)
    tuo.set_exclude_replies(False)
    tuo.set_include_rts(True)

    print(tuo.create_search_url())
    
    print( tuo.createSearchURL())

except TwitterSearchException as e:
      print(e)