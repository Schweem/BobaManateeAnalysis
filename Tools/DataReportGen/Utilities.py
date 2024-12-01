import csv

# getSceneTimes 
# args : fileName
# function for parsing CSV and calculating time spent in scenes 

def getSceneTimes(fileName):
    sceneData = {}
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] in ["sceneChange", "sceneCompleted"]:
                try:
                    sceneData[row[3]] = int(row[4])
                except ValueError:
                    sceneData[row[3]] = None
    sceneData["End Scene"] = getTimeInLastScene(fileName)
    return sceneData

def getUnderwaterSceneTime(fileName):
    """
    Calculates the total time spent in underwater scenes by excluding scenes 0 and 12.
    """
    underwaterTime = 0
    landScenes = ["0 - Boat Scene", "12 - Ending Boat Scene"]

    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Ensure we're processing relevant rows
            if row[0] in ["sceneChange", "sceneCompleted"]:
                try:
                    sceneName = row[3]
                    timeChange = int(row[4])

                    # Exclude scenes "0 - Boat Scene" and "12 - Ending Boat Scene"
                    if sceneName not in landScenes:
                        underwaterTime += timeChange
                except ValueError:
                    # Skip invalid time values
                    continue

    return underwaterTime

# getnameselected
# args : filename 
# function for retreiving the selected names of manatee friends 
# from the start of game on the boat. 
def getNamesSelected(fileName):
    names = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "manateeNameSelected":
                names.append(row[3])
    return names

# gettimespentoncanvases
# args : fileName
# function for parsing csv files for retreiving the total 
# time spent reading / looking at marked canvases or objects 

def getTimesSpentOnCanvases(fileName):
    allObjects = {}
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "lookingAt" and row[4] != "null":
                try:
                    time_spent = int(row[4])
                    slide_name = row[3].replace(';', '')
                    if slide_name in allObjects:
                        allObjects[slide_name] += time_spent
                    else:
                        allObjects[slide_name] = time_spent
                except ValueError:
                    continue
    return allObjects

# geteventtypecount
# args : fileName, eventType, seperationTime
# function for parsing csvs to count the occourance of a given event type. 

def getEventTypeCount(fileName, eventType, separationTime=0):
    eventCount = 0
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        lastEventTime = -1
        for row in reader:
            if row[0] == eventType:
                try:
                    event_time = int(row[1])
                    if event_time > lastEventTime + (separationTime * 1000):
                        eventCount += 1
                        lastEventTime = event_time
                except ValueError:
                    continue
    return eventCount

# gettimeinlastscene
# args : fileName
# function for parsing csv file, used for calcuating time spent in the last scene 
# useful until i make a log that sends before the game closes (thats a TODO now)

def getTimeInLastScene(fileName):
    time = 0
    lastTime = 0
    inScene = False
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "sceneChange" and not inScene:
                if row[3] == "12 - Ending Boat Scene":
                    try:
                        time -= int(row[4])
                        inScene = True
                    except ValueError:
                        continue
            elif inScene:
                try:
                    lastTime = int(row[4])
                except ValueError:
                    continue
    return (time + lastTime) / 1000

# getnumberofbreathes
# args : fileName
# function for parsing csv file to get the total number of times
# the player breathed during the simulation

def getNumberOfBreaths(fileName):
    """
    Counts the number of times the 'playerBreathe' event appears in the log file.
    """
    breatheCount = 0
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "playerBreathe":
                breatheCount += 1
    return breatheCount

# getsqueaksused
# args : fileName
# function for getting total number of times a player squeaked. 
# boilerplate, hookup

def getSqueaksUsed(fileName):
    return getEventTypeCount(fileName, "playerSqueak")

# getflipperbumps
# args : filename
# function for getting total number of flipper bumps from a session
# boilerplate, hookup

def getFlipperBumps(fileName):
    return getEventTypeCount(fileName, "flipperBump")

# gettimeinhuddle
# args : filename
# function for calculating total time spent huddling in a session
# boilerplate, hookup

def getTimeInHuddle(fileName):
    return getEventTypeCount(fileName, "huddleEnd")

# getpostboxsearchtime
# args : filename
# function for calculating time spent looking for the postbox in 
# fund your friends. 
# boilerplate, hookup. 

def getPostboxSearchTime(fileName):
    """
    Calculates the time difference between the end of the 'Multiplayer Lobby' scene
    and the timestamp when the player looks at the 'Mailbox'.
    """
    lobby_end_time = None
    mailbox_time = None

    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Capture the time for the end of the Multiplayer Lobby
            if row[0] == "sceneCompleted" and row[3] == "9 - MultiplayerLobby":
                try:
                    lobby_end_time = int(row[1])
                except ValueError:
                    continue

            # Capture the time when looking at the Mailbox
            if row[0] == "lookingAt" and row[3] == "Mailbox":
                try:
                    mailbox_time = int(row[1])
                except ValueError:
                    continue

            # If both times are found, calculate the difference
            if lobby_end_time is not None and mailbox_time is not None:
                break

    # Return the time difference in seconds (or None if data is incomplete)
    if lobby_end_time is not None and mailbox_time is not None:
        return round((lobby_end_time - mailbox_time), 0) 
    else:
        return None

# peanutmanateetime
# args : filename
# function for retrieving time spent looking at the sickly manatee in 
# manatee hell. 

def getPeanutManateeTime(fileName):
    """
    Returns time spent looking at peanut manatees in Manatee Hell.
    """
    
    peanutManatees = ["peanutHead00", "peanutHead01"]
    peanutLookingTime = 0
    
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "lookingAt" and row[3] in peanutManatees:
                try:
                    peanutLookingTime += int(row[4])
                except ValueError:
                    continue
                
    return peanutLookingTime
