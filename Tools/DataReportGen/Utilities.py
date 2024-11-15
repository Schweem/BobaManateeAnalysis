import csv

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

def getNamesSelected(fileName):
    names = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "manateeNameSelected":
                names.append(row[3])
    return names

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

def getTimeInLastScene(fileName):
    time = 0
    lastTime = 0
    inScene = False
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] == "sceneChange" and not inScene:
                if row[3] == "5 - End Scene":
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

def getSqueaksUsed(fileName):
    return getEventTypeCount(fileName, "playerSqueak")

def getFlipperBumps(fileName):
    return getEventTypeCount(fileName, "flipperBump")

def getTimeInHuddle(fileName):
    return getEventTypeCount(fileName, "huddleTime")

def getPostboxSearchTime(fileName):
    """
    Placeholder function for time spent finding the postbox.
    """
    return 0

def getPeanutManateeTime(fileName):
    """
    Placeholder function for time spent looking at peanut head manatee.
    """
    return 0