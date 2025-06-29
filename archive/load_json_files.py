import json
import glob

knowledge = []
for file_path in glob.glob("converted/*.json"):
    with open(file_path) as f:
        content = f.read()
    knowledge.append(content)

