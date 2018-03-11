from pymongo import MongoClient
import os
import json
import time



def connect():
    client = MongoClient('mongodb://root:toor@10.3.11.169:27017/')
    db = client.ucode2018
    return db

global db
db = connect()

def insert_Localizacion(db, lat, long):
    location_id = None
    while not location_id:
        location_id = db.lugares.find_and_modify(
            {"sitio": {"lat": lat, "long":long}},
            {"$set": {"sitio": {"lat": lat, "long":long}},
             },
            upsert=True, returnNewDocument=True, safe=True
        )
    return location_id

def insert_Localizacion_persona(db,location_id, persona_id):
    db.personas.update(
        {"_id": persona_id},
        {"$set": {
            "location": location_id}},
    )
    db.personas.update(
        {"_id": persona_id},
        {"$addToSet": {
            "location": {"$each": location_id}}},
    )

def insert_Persona(db, nick, name, profile_img, followers, friends):
    persona_id = None
    while not persona_id:
        persona_id = db.personas.find_and_modify(
            {"nick": nick},
            {"$set": {
                "nick": nick,
                "name": name,
                "sentinent": 0,
                "profile_img":profile_img,
                "followers":followers,
                "friends":friends
                }},
            upsert=True, returnNewDocument=True, safe=True
        )

    return persona_id

def insertar_gusto(db, like, hashtags):
    gusto_id = None
    while not gusto_id:
        gusto_id = db.gusto.find_and_modify(
            {"name": like},
            {"$addToSet": {
                'hashtags': {'$each': hashtags},
                },
            "$set": {
                "name": like}},
            upsert=True, returnNewDocument=True, safe=True
        )
    return gusto_id

def insertar_persona_gusto(db, gusto_id, persona_id, sentient):
    db.gustos.update(
        {"_id": gusto_id},
        {"$push": {
            "people": persona_id}}
    )
    result = db.personas.find_one({"_id": persona_id})

    db.personas.update(
        {"_id": persona_id},
        {"$addToSet": {
            "sentient": result['sentinent']+sentient,
            "like": gusto_id}}
    )


def insertar_evento(event, gusto_ids, date, lugar_id):
    global db
    evento_id = None
    while evento_id is None:
        evento_id = db.eventos.find_and_modify(
            {"name": event},
            {"$addToSet": {
                'like': {"$each": [gusto_ids]}},
                "$set": {
                    "name": event,
                    "date": date,
                    "lugar": lugar_id}},
            upsert=True, returnNewDocument=True
        )
    db.localizacion.update(
        {"_id": lugar_id},
        {"$addToSet": {
            "events": {"$each":[evento_id]}}},
    )
    for gusto in gusto_ids:
        #print(gusto)
        db.gustos.update(
            {"_id": gusto},
            {"$addToSet": {
                "events": {"$each":[evento_id]}}},
        )
    return evento_id["_id"]

def insertar_tweet_evento(persona, evento_id):
    global db
    nick, name, profile_img, followers, friends = persona
    persona_id = insert_Persona(db, nick, name, profile_img, followers, friends)
    add_persona_evento(db, persona_id["_id"], evento_id)

def add_persona_evento(db, persona_id, evento_id):
    db.eventos.update(
        {"_id": evento_id},
        {"$addToSet": {
            'people': {"$each":[persona_id]}}},
        upsert=True)

    db.personas.update(
        {"_id": persona_id},
        {"$addToSet": {
            "events": {"$each":[evento_id]}}},
    )


def add_imagen(db, img, gusto_id):
    gusto_id = db.gusto.update(
        {"_id": str(gusto_id)},
        {"$addToSet": {
            'img': {"$each":[img]}}},
        upsert=True)



def load_data(path, db):
    with open(path, 'r', encoding="utf8") as file:
        data = json.load(file)
    like = data["team"].split('.')[0]
    print(like)
    for user in data["data"]:
        nick = user["user"]["name"]
        name = user["user"]["nick"]
        profile_img = user["user"]["profile_img"]
        followers = user["user"]["followers"]
        friends = user["user"]["friends"]
        hashtag = user["hashtags"]
        sentient = user["sentient"]
        persona_id = insert_Persona(db, nick, name, profile_img, followers, friends)
        #print(persona_id)
        if user["user"]["location"] != {}:
            lat = user["user"]["location"]["lat"]
            long = user["user"]["location"]["long"]
            location_id = insert_Localizacion(db, lat, long)
            insert_Localizacion_persona(db, [location_id['_id']], persona_id['_id'])

        gusto_id = insertar_gusto(db,like,hashtag)
        #print(gusto_id)
        insertar_persona_gusto(db,gusto_id['_id'],persona_id['_id'],sentient)

def insert_location_from_data(path, db):
    with open(path, 'r', encoding="utf8") as file:
        data = json.load(file)
    for user in data["data"]:
        lat = user["user"]["location"]["lat"]
        long = user["user"]["location"]["long"]
        nick = user["user"]["name"]
        user_id = db.personas.find_one({"nick": nick})
        location_id = insert_Localizacion(db, lat, long)
        insert_Localizacion_persona(db, [location_id['_id']], user_id['_id'])

def load_matches(path, db):
    with open(path, 'r', encoding="utf8") as file:
        data = json.load(file)
    for team in data:
        away = team["Away_team"]
        home = team["Home_team"]
        lat = team["Location"]["lat"]
        long = team["Location"]["long"]
        date = team["Date"]
        home_id = db.gusto.find_one({"name": home})
        visit_id = db.gusto.find_one({"name": away})
        location_id = insert_Localizacion(db, lat,long)
        insertar_evento(away+'vs'+home,[home_id, visit_id],date,location_id)

def main():
    
    while True:
    #load_matches('../results.json', db)
        files = os.listdir('..\\DataAnalyser\\output\\')
        for file in files:
            load_data('../DataAnalyser/output/'+file, db)
            os.rename('../DataAnalyser/output/'+file, 'Data/'+file)
        time.sleep(300)