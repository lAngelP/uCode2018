# Extracción de una página web de información

import requests
def generate_hashtags(baselist):
    url= "http://d212rkvo8t62el.cloudfront.net/tag/"
    for base in baselist:
        one = baselist[base][1:]
        resp= requests.get(url=url+one)
        data= resp.json()
        baselist[base] = ['#'+hashtag['tag'] for hashtag in data['results']][:4]
        return baselist

"""
if __name__ == "__main__":
    generate_hashtags({"Realmadrid":"#realmadrid"})
"""
