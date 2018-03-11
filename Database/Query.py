from pymongo import MongoClient

def connect():
    client = MongoClient('mongodb://root:toor@localhost:27017/')
    db = client.ucode2018
    return db

def find_best(team, db=None):
    if not db:
        db = connect()
    gusto_id = db.gusto.find_one({'name': team})
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
    print(find_best('LAL'),db)
    print(find_best('DEN'),db)