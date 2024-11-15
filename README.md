## Boba Manatee Log Analysis Tool(s) 
Currently includes:
- Analysis script - `/Tools/dataRetrieval.py`
----

The analysis script uses an environment variable to connect to the hosted endpoint for the flask API that bridges the simulation to the mongoDB.

----

### Instructions for use 
- `Clone this repository`
- `Setup your .env file.` These means defining "BASE_URL" in your .env OR replacing the .env call with a static link to endpoint (Line 9)
  `(.env file goes in the 'Tools' directory along side the python script)`
- Install requirements `'pip install -r requirements.txt'` in the root directory
- Run `'dataRetrival.py'`

----

### Functionality 
Once run, the script will connect to the API and get a list of session IDs. It will then extract all the logs for each unique session ID and 
generate a csv report of the log data. These CSV reports are then used by the report generation script (soon to come).
