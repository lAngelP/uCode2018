from pymongo import MongoClient
import os
import json
import time
def connect():
    client = MongoClient('mongodb://root:toor@localhost:27017/')
    db = client.ucode2018
    return db

def find_best(teamn_id):
    results = db.personas.find({'%set.like': gusto_id["_id"]})
    results = [result for result in results]
    dic = {}
    for result in results:
        list = result['%set']
        for set in list:
            if set['like'] == gusto_id['_id']:
                dic[result['nick']] = set['sentinent']

    end = [(k, dic[k]) for k in sorted(dic, key=dic.get, reverse=True)]
    return end

if __name__ == '__main__':
    db = connect()
    gusto_id = db.gusto.find_one({'name':'LAL'})
    print('LAL')
    print(find_best(gusto_id))
    gusto_id = db.gusto.find_one({'name': 'DEN'})
    print('DEN')
    print(find_best(gusto_id))