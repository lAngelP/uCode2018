from flask import Flask

app = Flask(__name__)

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

@app.route('/createt-shirt')
def generatet_shirt():
    resp = Flask.make_response(app, load_binary("logo-eina.png"))
    resp.headers['Content-Type'] = 'image/png'

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')