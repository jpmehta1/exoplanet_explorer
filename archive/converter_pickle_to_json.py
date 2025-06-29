import os
import json
import pickle
import pandas as pd

# Define the directory where your pickle files are
directory = "answers"           # Change if your .pkl files are in another folder
output_dir = "converted"        # Where .json files will be saved

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through and convert
for file in os.listdir(directory):
    if file.endswith(".pkl"):
        with open(os.path.join(directory, file), "rb") as f:
            data = pickle.load(f)

        output_path = os.path.join(output_dir, file.replace(".pkl", ".json"))
        if isinstance(data, pd.DataFrame):
            data.to_json(output_path, orient="records", lines=True)
        else:
            with open(output_path, "w") as out:
                json.dump(data, out, indent=2)

print("✅ Conversion complete. JSON files saved in:", output_dir)

