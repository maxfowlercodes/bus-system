import requests
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import webbrowser
import gmplot
import csv
import pandas
import pyautogui
import time
from io import StringIO


vehiclelats = []
opened = False
count = 0
vehiclelongs = []
load_dotenv()

BODS_API_KEY = os.getenv("BODS_API_KEY")
apikey = os.getenv("MAPS_API")

params = {
    "api_key": BODS_API_KEY,
    "boundingBox": "-2.80,51.35,-2.45,51.57"
}
for x in range(10):
    url = "https://data.bus-data.dft.gov.uk/api/v1/gtfsrtdatafeed/"
    data = pandas.read_csv("trips.csv")     
    response = requests.get(url, params=params)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    gmap3 = gmplot.GoogleMapPlotter(
        51.455989,
        -2.592673,
        12,
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
                    direction = filtered_data.iloc[0]["direction_id"]
                    
                    print("Vehicle ID: ", vehicle_id)
                    print("Route: ", routeID)
                    print("Destination ID: ", direction)
                    vehiclelats.append(vehiclelat)
                    vehiclelongs.append(vehiclelong)
                    
                    
                    if direction == 1:
                        gmap3.marker(vehiclelat, vehiclelong, title=routeID + " to Cribbs Causeway " + vehicle_id, color="blue")
                        print("Bus logged to Cribbs")
                    elif direction == 0:
                        gmap3.marker(vehiclelat, vehiclelong, title=routeID + " to Broadmead " + vehicle_id, color="red")
                        print("Bus logged to City Centre")
                    else:
                        print("Failed marker")
                else:
                    print("Removed odd bus")
                    
                    
    gmap3.draw(r"C:\Users\maxfo\Desktop\Bus System\map3.html")
    count = count + 1
    if opened == False:
        webbrowser.open_new_tab(r"C:\Users\maxfo\Desktop\Bus System\map3.html")
        opened = True
    else:
        pyautogui.hotkey('f5')
        time.sleep(15)

print(f"Ran {count} times")
