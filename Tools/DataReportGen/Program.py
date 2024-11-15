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

            # Multiplayer metrics
            "Squeaks Used": squeaksUsed,
            "Flipper Bumps": flipperBumps,
            "Time in Huddle": huddleTime,

            # Totals
            "Total underwater time": sum(sceneTimes.values()) * 1000, # TODO : make this scenes 1-11
            "Total game time": sum(sceneTimes.values()) * 1000, # TODO : make this scenes 0 and 12 
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