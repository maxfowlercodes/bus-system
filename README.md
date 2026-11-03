
# Bus Tracking system

**Please note this system is currently only built for the No.1 Bus service within Bristol**

Before running the python script please install the dependancies. 
>pip install gtfs-realtime-bindings gmplot python-dotenv

Please ensure you have a .env file with your API key for BODS and Google Maps.

>BODS - https://data.bus-data.dft.gov.uk/guidance/requirements/?section=api

>Maps - https://console.cloud.google.com/google/maps-apis/

To run this script please pull the repo into a folder either by downloading it, using the GH CLI or using git. 

Press **Code** and click **Download ZIP:**
https://github.com/maxfowlercodes/bus-system
**GH CLI**
\\\gh repo clone maxfowlercodes/bus-system
**Git**
\\\git clone https://github.com/maxfowlercodes/bus-system.git

When running the system it will first connect to the BODS API, to locate the busses currently running on the No.1 Route. 
It will gather the ID for each of them, and their latititude and longditude. It will then use google maps to place these co-ordinates. 
Please note it can take a few seconds to start up, and sometimes a wrong bus is picked up, but this is being looked into and there is continued work on it. 