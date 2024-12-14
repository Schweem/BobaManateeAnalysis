## Boba Manatee Log Analysis Tool(s) 
Tools built for the Boba Manatee Simulation. Analysis tools for collecting data logs and building csv reports, as well as the server API script used on the deployed server. Developed by Seamus Jackson working under the direction of Tania Roy at New College of Florida. 

Currently includes:
- Analysis script - `/Tools/dataRetrieval.py`
- Report generation tools - `/Tools/program.py, utilities.py`
- Server API script - `/Tools/BobaServer/bobabackend.py`
----

- The analysis script uses an environment variable to connect to the hosted endpoint for the flask API that bridges the simulation to the mongoDB.

- The server script is included. This is deployed at a fixed endpoint, running the server locally would require a modification to the API url in the simulation itself in the `TelemetryManger` object in the first scene. 

----

### Instructions for use 

## Setting up

- `Ensure Python 3.11+ is installed`
- `Clone this repository`
- `Setup your .env file.` These means defining "BASE_URL" in your .env OR replacing the .env call with a static link to endpoint (Line 9)
  `(.env file goes in the 'Tools' directory along side the python script)`
    - https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/
- Install requirements `'pip install -r requirements.txt'` in the root directory (These are for both server and analysis)

## Collecting Data from the server 
- Run `'dataRetrieval.py'`, to pull data and build csv reports.
  - Ensure .env file is prepared
 
## Generating reports from server data 
- Run `program.py` to generate aggregate summaries and individual csv reports from the data produced by `dataretrieval.py`
  - `This script functions by taking the data pulled from running dataRetrieval.py and uses it for individual and aggregate report generation. Please ensure that you have done one of the following before running this script`
    - Setup a .env file as described above and run `dataRetrieval.py` to pull logs from the backend server.
    - Alternativley, if you have `Collected data locally on the headset`, please copy it from the headset into a directory called `telemetry_reports`, you do this in place of the the retreival script creating that directory for you.
  - With a present telemtry reports directory the script will read in all of the data and produce individually formatted csv reports as well as an aggregate excel summary of the session.   

----

### Functionality 
- Once run, the analysis script will connect to the API and get a list of session IDs. It will then extract all the logs for each unique session ID and generate a csv report of the log data. These CSV reports are then used by the report generation script (soon to come).
- Running the server script will host the API, generally this isnt going to be the case. Ideally it is deployed via docker, DOCKERFILE included (mongoURI not included).
- The report generation tools are the final step of the pipeline. Once the data has been collected from the DB the python scripts are used to parse the data and produce reports. 
