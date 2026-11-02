import requests
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import webbrowser
import gmplot

vehiclelats = []
vehiclelongs = []

load_dotenv()

BODS_API_KEY = os.getenv("BODS_API_KEY")
apikey = os.getenv("MAPS_API")

params = {
    "api_key": BODS_API_KEY,
    "boundingBox": "-2.80,51.35,-2.45,51.57"
}

url = "https://data.bus-data.dft.gov.uk/api/v1/gtfsrtdatafeed/"

response = requests.get(url, params=params)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
gmap3 = gmplot.GoogleMapPlotter(
    51.455989,
    -2.592673,
    18,
    apikey=apikey
)

print(response.status_code)

for entity in feed.entity:
    if entity.HasField("vehicle"):
        vehicle = entity.vehicle
        vehicleid = vehicle.trip.route_id
        vehiclelat = vehicle.position.latitude
        vehiclelong = vehicle.position.longitude

        if vehicleid == "120483" or vehicleid == "120729" or vehicleid == "120860":
            print("Vehicle ID: ", vehicle.vehicle.id)
            print("Route: ", vehicle.trip.route_id)
            
            vehiclelats.append(vehiclelat)
            vehiclelongs.append(vehiclelong)
            


gmap3.scatter(vehiclelats, vehiclelongs, '#FF0000', size = 40, marker = False)
gmap3.draw(r"C:\Users\maxfo\Desktop\Bus System\map3.html")
webbrowser.open_new_tab(r"C:\Users\maxfo\Desktop\Bus System\map3.html")