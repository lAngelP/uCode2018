from flask import Flask
import json
import codecs

app = Flask(__name__)

def load_file(name):
    with codecs.open("static/" + name, "r", encoding="utf-8") as f:
        return "".join(f.readlines())

def load_template(name):
    with open("templates/" + name + ".template", "r") as f:
        return "".join(f.readlines())

# Returns the HTML code to generate a heatmap
@app.route('/heatmap/')
def hello_a():
    data = json.loads(load_file("ATL.json"))["data"]
    locations = list(filter(lambda x: len(x) > 0, [data2["user"]["location"] for data2 in data]))
    print(locations)
    coords = [(locs['lat'], locs['long']) for locs in locations]
    print(coords)
    # coords = [(37.782551, -122.445368), (37.782745, -122.444586), (37.782842, -122.443688),
    #           (37.782919, -122.442815), (37.783100, -122.441461)]
    parsed_coords = ",".join([ "new google.maps.LatLng("+str(lat)+", "+str(lng)+")" for (lat, lng) in coords])

    template = load_template("heatmap")
    return template.replace("{{COORDINATES}}", parsed_coords)


#new google.maps.LatLng(37.782551, -122.445368)

@app.route('/createt-shirt')
def generatet_shirt():
    return 0

if __name__ == '__main__':
    app.run()