from flask import Flask
from flask import request
from time import *
import json
import codecs

app = Flask(__name__)

@app.route('/create_tshirt')
def generatet_shirt():
    sleep(5)
    return request.args.get('url')
    

if __name__ == '__main__':
    app.run()