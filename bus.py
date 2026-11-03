import requests
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import webbrowser
import gmplot

vehiclelats = []
vehiclelongs = []
count = 0
oddbus_count = 0
buscheck = ""


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
        routeID = vehicle.trip.route_id
        vehiclelat = vehicle.position.latitude
        vehiclelong = vehicle.position.longitude
        vehicleid = vehicle.vehicle.id
        licenseplate = vehicle.vehicle.license_plate
        destination = vehicle.trip.trip_id

    if routeID == "120483" or routeID == "120729" or routeID == "120860":
        short_name = "Number 1 Bus - Bristol"
        if vehicleid == "FBRI-30195" or vehicleid == "FBRI-30193":

            oddbus_count = oddbus_count + 1

            f = open(r"C:\Users\max.fowler.589_acces\Desktop\py\bus\tripstest.txt", "r")
            buscheck = f.read().strip()


                
        else:
            print("Vehicle ID: ", vehicleid)
            print("Route: ", vehicle.trip.route_id)

            if vehicle.trip.trip_id == buscheck:
                print(f"{vehicle.trip.trip_id} and {vehicleid} Going to cribbs")

            print(vehicle.trip.trip_id)

            
            count = count + 1

            gmap3.marker(vehiclelat, vehiclelong, title=vehicleid + " " + short_name)


f.close()
print(f"Found {count} buses.")
gmap3.draw(r"map3.html")
webbrowser.open_new_tab(r"map3.html")
print(buscheck)