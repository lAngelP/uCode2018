from pymongo import MongoClient
import json
def connect():
    client = MongoClient('mongodb://root:toor@localhost:27017/')
    db = client.ucode2018
    return db





def insertar_tweet(tweet, db):
    location = 'test_location'
    nick = 'test_nick'
    name = 'test_name'
    image = 'test_url'
    like = 'test_like'
    hashtags = ['hashtag1', 'hashtag2']

    location_id = db.lugares.find_one_and_update(
        {"sitio": location},
        {"$set": {"sitio": location}},
        upsert=True, returnNewDocument=True
    )
    persona_id = db.persona.find_one_and_update(
        {"nick": nick},
        {"$set":{
            "nick": nick,
            "name": name,
            "location": str(location_id['_id'])}},
        upsert=True, returnNewDocument=True
    )
    db.localizacion.update(
        {"_id": str(location_id['_id'])},
        {"$addToSet": {
            "population": nick}},
    )
    gusto_id = db.persona.find_one_and_update(
        {"name": like},
        {"$addToSet": {
            'hashtags': hashtags,
            'followers': str(persona_id['_id'])},
        "$set": {
            "name": like}},
        upsert=True, returnNewDocument=True
    )

def insertar


if __name__ == "__main__":
    db = connect()
    with open('../test-search/data/NBA/BrooklynNets.json', 'r') as file:
        data = json.load(file)
    for file in data:
        insertar_tweet(file, db)