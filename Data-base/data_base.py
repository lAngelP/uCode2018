from pymongo import MongoClient
import json
def connect():
    client = MongoClient('mongodb://root:toor@localhost:27017/')
    db = client.ucode2018
    return db

def insertPerson_Localization(db, location, nick, name):
    location_id = db.lugares.find_one_and_update(
        {"sitio": location},
        {"$set": {"sitio": location}},
        upsert=True, returnNewDocument=True
    )
    persona_id = db.personas.find_one_and_update(
        {"nick": nick},
        {"$set": {
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
    return location_id, persona_id

def insertar_gusto(db, like, hashtags, persona_id):
    gusto_id = db.gusto.find_one_and_update(
        {"name": like},
        {"$addToSet": {
            'hashtags': hashtags,
            'followers': str(persona_id['_id'])},
        "$set": {
            "name": like}},
        upsert=True, returnNewDocument=True
    )
    return gusto_id

def insertar_evento(db, event, gusto_id,date, lugar_id):

    evento_id = db.eventos.find_one_and_update(
        {"name": event},
        {"$addToSet": {
            'like': [str(gusto['_id']) for gusto in gusto_id]},
            "$set": {
                "name": event,
                "date": date,
                "lugar": str(lugar_id['_id'])}},
        upsert=True, returnNewDocument=True
    )
    db.localizacion.update(
        {"_id": str(lugar_id['_id'])},
        {"$addToSet": {
            "events": str(evento_id['_id'])}},
    )
    for gusto in gusto_id:
        print(gusto)
        db.gustos.update(
            {"_id": str(gusto['_id'])},
            {"$addToSet": {
                "events": str(evento_id['_id'])}},
        )
    return evento_id


def add_persona_evento(db, persona_id, evento_id):
    db.eventos.update(
        {"_id": str(evento_id['_id'])},
        {"$addToSet": {
            'people': str(persona_id['_id'])}},
        upsert=True)
    
    db.personas.update(
        {"_id": str(persona_id['_id'])},
        {"$addToSet": {
            "events": str(evento_id['_id'])}},
    )


def add_imagen(db, img, gusto_id):
    gusto_id = db.gusto.update(
        {"_id": str(gusto_id['_id'])},
        {"$addToSet": {
            'img': img}},
        upsert=True)

if __name__ == "__main__":
    db = connect()
    with open('../test-search/data/NBA/BrooklynNets.json', 'r') as file:
        data = json.load(file)
    location = 'testing_location'
    nick = 'testing_nick'
    name = 'testing_name'
    like = 'testing_gusto'
    date = '20181102'
    event = 'test_event'
    id = 'id_test'
    hashtag = ['#hashtag', '#hash2']
    location, persona = insertPerson_Localization(db,location, nick, name)
    gusto = insertar_gusto(db, like, hashtag, persona)
    insertar_evento(db,event, [gusto] ,date, location)