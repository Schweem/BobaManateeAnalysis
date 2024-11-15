from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv() # load environment variables

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient(os.getenv("MONGOURI")) # call the MONGOURI from the .env file, alternativly hardcode and assign link 

# define db and collections
db = client["TelemetryDB"]
telemetry_collection = db["TelemetryCollection"]
sessions_collection = db["sessions"]

### For sending data, these are used by the simulation to talk to the API and the DB ###

# saveTelemetry
# args : none 
# Used to send telemtry data from the simulation to the database. 
@app.route("/saveTelemetry", methods=["POST"])
def save_telemetry():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Insert data into the telemetry collection
        telemetry_document = {
            "sessionId": data.get("sessionId"), # sessionID 
            "name": data.get("name"), # name of log 
            
            "target": data.get("target", ""), # lookingAt target
            "time": data.get("time"), # time stamp
            "timestamp": datetime.utcnow(), # date time
            "textContent": data.get("textContent", ""), # text content like manatee name 
            "vec": data.get("vec", None), # vector data like a position
            "intContent": data.get("intContent", 0), # int content, often represents time in MS 
        }

        telemetry_collection.insert_one(telemetry_document)
        return jsonify({"message": "Telemetry saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# startSession
# args : None
# Start a new session, store the session ID in the database alongside the start time and sim version
@app.route("/startSession", methods=["POST"])
def start_session():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        session_document = {
            "sessionId": str(ObjectId()),
            "simulation": data.get("simulation", "Unknown"),
            "startTime": datetime.utcnow(),
        }
        sessions_collection.insert_one(session_document)
        return jsonify({"sessionId": session_document["sessionId"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        
### For retrieving data, this will be used by the collection and analysis script(s) ###

# getSessionIds
# args : None
# Used to produce a list of session IDs from the database. 
@app.route("/getSessionIds", methods=["GET"])
def get_session_ids():
    try:
        # store a list of unique session IDs
        session_ids = sessions_collection.distinct("sessionId")
        return jsonify({"sessionIds": session_ids}), 200 # return that list as a JSON object 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# getTelemetryBySessionId
# args : session_id
# Used to query the mongoDB for all documents associated with a given session. 
@app.route("/getTelemetryBySessionId/<session_id>", methods=["GET"])
def get_telemetry_by_session_id(session_id):
    try:
        # Find all telemetry documents associated with the given ID
        telemetry_logs = list(telemetry_collection.find({"sessionId": session_id}, {"_id": 0}))
        return jsonify({"telemetryLogs": telemetry_logs}), 200 # return them as JSON 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)