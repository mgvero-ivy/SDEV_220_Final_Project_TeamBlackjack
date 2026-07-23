import sqlite3
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

def get_connection():
    # Opens a connection to the SQLite database
    return sqlite3.connect("data.db")


def fill_table_from_waitlist(table, waitlist):
    """
    Checks whether a table has open seats.
    If it does, moves matching players from the waitlist to the table.
    """

    seated_players = []

    # Keep seating players while the table has open seats
    while table.seats_full < table.seats:

        player_found = False

        for player in waitlist:

            # Updated to match the attribute name in models.py
            if player.table_waiting_for == table.table_num:

                table.seats_full += 1
                seated_players.append(player)
                waitlist.remove(player)

                player_found = True
                break

        # Stop if nobody on the waitlist is waiting for this table
        if not player_found:
            break

    return seated_players


def remove_player_from_table(table, phone_number, players):
    """
    Removes a player from a table and updates the table seat count.
    """

    for player in players:

        # Updated to use phone_number and the models.py attribute names
        if (
            player.phone_number == phone_number
            and player.current_table == table.table_num
        ):
            player.current_table = None
            player.actively_playing = False

            if table.seats_full > 0:
                table.seats_full -= 1

            return True

    return False