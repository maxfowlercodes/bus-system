import requests
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import webbrowser
import gmplot
import csv
import pandas

from io import StringIO


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
data = pandas.read_csv("trips.csv")     
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
        routeID = vehicle.trip.route_id
        vehiclelat = vehicle.position.latitude
        vehiclelong = vehicle.position.longitude
        vehicledestination = vehicle.trip.trip_id
        vehicle_id = vehicle.vehicle.id

        if routeID == "120483" or routeID == "120729" or routeID == "120860":
            
            if vehicle_id != "FBRI-30195" and vehicle_id != "FBRI-30193" and vehicle_id != "FBRI-37425" and vehicle_id != "FBRI-39439" and routeID != "FBRI-39408":
                filtered_data = data[data["trip_id"] == vehicledestination]
                headsign = filtered_data.iloc[0]["trip_headsign"]
                
                print("Vehicle ID: ", vehicle_id)
                print("Route: ", routeID)
                print("Destination: ", headsign)
                vehiclelats.append(vehiclelat)
                vehiclelongs.append(vehiclelong)
                
                
                if headsign == "Broomhill":
                    gmap3.marker(vehiclelat, vehiclelong, title=routeID + " to " + headsign + " " + vehicle_id, color="blue")
                elif headsign == "Cribbs Causeway":
                    gmap3.marker(vehiclelat, vehiclelong, title=routeID + " to " + headsign + " " + vehicle_id, color="red")
                else:
                    print("Failed marker")
            else:
                print("Removed odd bus")

          



gmap3.draw(r"C:\Users\maxfo\Desktop\Bus System\map3.html")
webbrowser.open_new_tab(r"C:\Users\maxfo\Desktop\Bus System\map3.html")