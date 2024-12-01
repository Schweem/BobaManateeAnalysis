import Utilities
import os
import pandas as pd

input_dir = "telemetry_reports"
output_file = "Output/Aggregated_Server_Data_Stats.xlsx"
individual_summaries_dir = "Output"

# Ensure the directory for individual summaries exists
os.makedirs(individual_summaries_dir, exist_ok=True)

data = []

for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        filePath = os.path.join(input_dir, filename)
        participant_id = filename.split('.')[0]

        # Collect data for each participant
        sceneTimes = Utilities.getSceneTimes(filePath)
        underWaterTime = Utilities.getUnderwaterSceneTime(filePath)
        
        namesSelected = Utilities.getNamesSelected(filePath)
        timesOnCanvases = Utilities.getTimesSpentOnCanvases(filePath)
        grassesEaten = Utilities.getEventTypeCount(filePath, "seagrassEaten")
        numberOfBreaths = Utilities.getNumberOfBreaths(filePath)
        manateeInteractions = Utilities.getEventTypeCount(filePath, "manateeInteraction")
        
        squeaksUsed = Utilities.getSqueaksUsed(filePath)
        flipperBumps = Utilities.getFlipperBumps(filePath)
        peanutManateeTime = Utilities.getPeanutManateeTime(filePath)
        huddleTime = Utilities.getTimeInHuddle(filePath)

        # Aggregate data
        participant_data = {
            "Participant ID": participant_id,

            # Boat scene metrics
            "Boat scene - Total time": sceneTimes.get("0 - Boat Scene", 0) * 1000,
            "Text Canvas Slide 0 - Reading time": timesOnCanvases.get("Slide 0 - Introduction", 0),
            "Text Canvas Slide 2 - Reading time": timesOnCanvases.get("Slide 2 - Manatee Social Behavior", 0),
            "Text Canvas Slide 3 - Reading time": timesOnCanvases.get("Slide 3 - Manatee Diet/Sound", 0),
            "Chosen Names": ', '.join(namesSelected),

            # Underwater tutorial metrics
            "Manatee scene - Learning controllers time": sceneTimes.get("1 - Underwater Tutorial", 0) * 1000,
            "Underwater tutorial - Total time": sceneTimes.get("1 - Underwater Tutorial", 0) * 1000,

            # Manatee life scene metrics
            "Manatee life scene - Total time": sceneTimes.get("2 - Manatee Life", 0) * 1000,
            "Number of Seagrass Eaten": grassesEaten,
            "Number of Breaths": numberOfBreaths,
            "Number of Manatee Interactions": manateeInteractions,
            "Mangrove popup - Viewing time": timesOnCanvases.get("MangrovePopup", 0),
            "Fish popup - Viewing time": timesOnCanvases.get("FishPopup", 0),
            "Seagrass popup - Viewing time": timesOnCanvases.get("SeaGrassPopup", 0),

            # Manatee school metrics
            "Manatee school Slide 2 - Reading time": timesOnCanvases.get("Slide 2 - Pollution Sources", 0),
            "Manatee school Slide 3 - Reading time": timesOnCanvases.get("Slide 3 - Algae Blooms", 0),
            "Manatee school Slide 4 - Reading time": timesOnCanvases.get("Slide 4 - Seagrass Loss", 0),
            "Manatee school Slide 5 - Reading time": timesOnCanvases.get("Slide 5 - Manatee Mortality", 0),
            "Manatee school Slide 6 - Reading time": timesOnCanvases.get("Slide 6 - Human Help Is Needed", 0),
            "Manatee school Slide 7 - Reading time": timesOnCanvases.get("Slide 7 - Keep an Eye Out for Pollution", 0),
            "Manatee school - Total Reading time": sum([
                timesOnCanvases.get("Slide 2 - Pollution Sources", 0),
                timesOnCanvases.get("Slide 3 - Algae Blooms", 0),
                timesOnCanvases.get("Slide 4 - Seagrass Loss", 0),
                timesOnCanvases.get("Slide 5 - Manatee Mortality", 0),
                timesOnCanvases.get("Slide 6 - Human Help Is Needed", 0),
                timesOnCanvases.get("Slide 7 - Keep an Eye Out for Pollution", 0)
            ]),
            "Manatee school - Total time": sceneTimes.get("4 - ManateeSchool", 0) * 1000,

            # Manatee Hell metrics
            "Manatee Hell - Peanuthead viewing time": peanutManateeTime,
            "Seagrass eating time in Manatee Hell": grassesEaten,  # Reusing count for now
            "Total time in Manatee Hell": sceneTimes.get("5 - V2 ManateeHell", 0) * 1000,
            "Mail box - Viewing time": timesOnCanvases.get("Mailbox", 0),
            "Mail box - Search Time":Utilities.getPostboxSearchTime(filePath),
            
            # New location school metrics 
            "Tampa Bay school Slide 1 - Reading time": timesOnCanvases.get("Slide 1 - distance travelled", 0),
            "Tampa Bay school Slide 2 - Reading time": timesOnCanvases.get("Slide 2 - water quality", 0),
            "Tampa Bay school Slide 3 - Reading time": timesOnCanvases.get("Slide 3 - seagrass", 0),
            "Tampa Bay school Slide 4 - Reading time": timesOnCanvases.get("Sl;ide 4 - Seagrass Loss", 0),
            "Tampa Bay school Slide 5 - Reading time": timesOnCanvases.get("Slide 7 - Keep an Eye Out for Pollution", 0),
            "Tampa Bay school - Total Reading time": sum([
                timesOnCanvases.get("Slide 1 - distance travelled", 0),
                timesOnCanvases.get("Slide 2 - water quality", 0),
                timesOnCanvases.get("Slide 3 - seagrass", 0),
                timesOnCanvases.get("Sl;ide 4 - Seagrass Loss", 0),
                timesOnCanvases.get("Slide 7 - Keep an Eye Out for Pollution", 0)
            ]),
            "Tampa bay school time": sceneTimes.get("7 - NewLocationSchool", 0) * 1000,
            
            # boat hit scene 
            "Boat Hit - Total time": sceneTimes.get("8 - Boat Hit Scene", 0) * 1000,
            "Looking at Hit Manatee": timesOnCanvases.get("Cutscene Manatee (Boat hit)", 0),
            
            # multi player lobby scene 
            "Multiplayer Lobby - Total time": sceneTimes.get("9 - MultiplayerLobby", 0) * 1000,

            # Multiplayer metrics
            "Squeaks Used": squeaksUsed,
            "Flipper Bumps Initiated": flipperBumps,
            "Times Initiated Huddle": huddleTime,
            
            "Find My Friends - Total time": sceneTimes.get("10 - Find Your Friends", 0) * 1000,
            
            # End scene metrics
            "End Scene - Waving Manatee looking time": timesOnCanvases.get("Waving Manatee", 0),
            "End Scene - Reading Time": timesOnCanvases.get("Conclusion Text", 0),

            # Totals
            "Total underwater time": underWaterTime * 1000,
            "Total game time": sum(sceneTimes.values()) * 1000,
        }

        # Append data for each participant
        data.append(participant_data)

        # Save individual summary
        individual_output_file = os.path.join(individual_summaries_dir, f'{participant_id}_summary.csv')
        pd.DataFrame([participant_data]).to_csv(individual_output_file, index=False)

# Create DataFrame for all participants
df = pd.DataFrame(data)

# Save aggregated data
df.to_excel(output_file, index=False)

print(f"Aggregated data saved to {output_file}")
print(f"Individual summaries saved to {individual_summaries_dir}")