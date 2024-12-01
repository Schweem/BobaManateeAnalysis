import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv() # load environemt variables (just url for API as of now)

# Base URL for the API
BASE_URL = os.getenv("ENDPOINT_URL", "http://127.0.0.1:5000") # load URL from .env file. alternativley, replace and hardcode url 

# get_session_ids
# args : none
# Function to get all unique session IDs. Useful for pulling reports. 
def get_session_ids():
    try:
        response = requests.get(f"{BASE_URL}/getSessionIds") # ping the API
        response.raise_for_status()
        session_ids = response.json().get("sessionIds", []) # store the session IDs
        return session_ids # return them
    except Exception as e: # if something goes wrong throw exception
        print(f"Error fetching session IDs: {e}")
        return []

# get_telemetry_logs
# args : session_id (session you want data from)
# Function to get telemetry logs by session ID
def get_telemetry_logs(session_id):
    try:
        response = requests.get(f"{BASE_URL}/getTelemetryBySessionId/{session_id}") # ping API
        response.raise_for_status()
        telemetry_logs = response.json().get("telemetryLogs", []) # store logs 
        return telemetry_logs # return them
    except Exception as e: # you know what this is
        print(f"Error fetching telemetry logs for session ID {session_id}: {e}")
        return []
        
# generate_csv_report
# args : session_id (target session), telemetry_logs (collected via session_id)
# Function to generate a CSV report for a session
def generate_csv_report(session_id, telemetry_logs):
    # Define the CSV file name
    csv_filename = f"{session_id}_logs.csv"
    
    # Define the header for the CSV
    header = ["name", "time", "vec", "textContent", "intContent"]
    
    # Write the telemetry logs to a CSV file
    try:
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for log in telemetry_logs:
            	
                # pre flight checks, ensure nice and clean data is writen
            	# textContent handles turning the target from lookingAt logs into textContent. This ensures backwards compatibility with analysis.py
            	
            	# we check the vector data ahead of time too, only writing it out if the data is not default 
            	
                text_content = log.get("textContent", "") # check the text content 
                if not text_content and "target" in log: # if the text content is empty but theres a target (lookingAt)
                    text_content = log["target"] # write the target to textContent
                    
                vec = log.get("vec", "") # check the vector content
                if vec == {'x': 0.0, 'y': 0.0, 'z': 0.0}: # if its the default value
                    vec = "" # dont write, keeps logs cleaner (this is how the old one worked)
            	
                # Write only fields that match the header
                writer.writerow({
                    "name": log.get("name", ""),
                    "time": log.get("time", ""),
                    "vec": vec,
                    "textContent": text_content,
                    "intContent": log.get("intContent", "")
                })
        print(f"CSV report generated: {csv_filename}")
    except Exception as e:
        print(f"Error writing CSV for session ID {session_id}: {e}")

# Main function to aggregate data and generate reports
def main():
    try:
        # Fetch all session IDs
        session_ids = get_session_ids()
        if not session_ids:
            print("No session IDs found. Exiting.")
            return

        # Create a directory for the reports
        reports_dir = "telemetry_reports"
        os.makedirs(reports_dir, exist_ok=True)
        os.chdir(reports_dir)
    
        # Fetch telemetry logs for each session and generate a report
        for session_id in session_ids:
            print(f"Processing session ID: {session_id}")
            telemetry_logs = get_telemetry_logs(session_id)
            if telemetry_logs:
                generate_csv_report(session_id, telemetry_logs)
            else:
                print(f"No telemetry logs found for session ID: {session_id}")
    except Exception as e:
    	print(f"CRITICAL ERROR, maybe install dependancies? : {e}")
    	
if __name__ == "__main__":
    main()
