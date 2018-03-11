from flask import Flask, request
import time
import random

app = Flask(__name__)

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

@app.route('/createt_shirt')
def generatet_shirt():
    time.sleep(3)
    res = Flask.make_response(app, load_binary("img/final"+str(random.randint(1,4))+".jpg"))
    res.headers['Content-Type'] = 'image/jpg'
    
    return res

if __name__ == '__main__':
    app.run(port=8080)