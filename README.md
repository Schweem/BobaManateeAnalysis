## Boba Manatee Log Analysis Tool(s) 
Tools built for the Boba Manatee Simulation. Analysis tools for collecting data logs and building csv reports, as well as the server API script used on the deployed server. Developed by Seamus Jackson working under the direction of Tania Roy at New College of Florida. 

Currently includes:
- Analysis script - `/Tools/dataRetrieval.py`
- Server API script - `/Tools/BobaServer/bobabackend.py`
----

- The analysis script uses an environment variable to connect to the hosted endpoint for the flask API that bridges the simulation to the mongoDB.

- The server script is included. This is deployed at a fixed endpoint, running the server locally would require a modification to the API url in the simulation itself in the `TelemetryManger` object in the first scene. 

----

### Instructions for use 
- `Clone this repository`
- `Setup your .env file.` These means defining "BASE_URL" in your .env OR replacing the .env call with a static link to endpoint (Line 9)
  `(.env file goes in the 'Tools' directory along side the python script)`
- `An additional ENV file is used in the server API, this will include MONGOURI the endpoint for mongoDB`
- Install requirements `'pip install -r requirements.txt'` in the root directory (These are for both server and analysis)
  
- Run `'dataRetrival.py'`, to pull data and build csv reports.
- Run `'bobabackend'` to host the API locally 

----

### Functionality 
- Once run, the analysis script will connect to the API and get a list of session IDs. It will then extract all the logs for each unique session ID and generate a csv report of the log data. These CSV reports are then used by the report generation script (soon to come).
- Running the server script will host the API, generally this isnt going to be the case. Ideally it is deployed via docker, DOCKERFILE to come. 
