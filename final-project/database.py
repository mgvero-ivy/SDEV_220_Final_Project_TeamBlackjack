import json
from pathlib import Path

# Finds data.txt in the same folder as database.py
DATA_FILE = Path(__file__).parent / "data.txt"


def load_data():
    """
    Reads all table and player data from data.txt.
    Returns the data as a Python dictionary.
    """

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        # Return an empty structure if the file does not exist
        return {"tables": []} 

    except json.JSONDecodeError:
        # Return an empty structure if the JSON is invalid
        return {"tables": []}


def save_data(data):
    """
    Saves the table and player data back into data.txt.
    """

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

