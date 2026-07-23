import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLAYERS_FILE = os.path.join(DATA_DIR, "players.txt")
WAITLIST_FILE = os.path.join(DATA_DIR, "waitlist.txt")
TABLES_FILE = os.path.join(DATA_DIR, "tables.txt")
HISTORY_FILE = os.path.join(DATA_DIR, "history.txt")

def fill_table_from_waitlist(table, waitlist):
    """
    Checks whether a table has open seats.
    If it does, seats players from the waitlist.
    """

    seated_players = []

    while table.seatsfull < table.seats:

        player_found = False

        for player in waitlist:

            if player.tablewaitingfor == table.tablenum:

                table.seatsfull += 1
                seated_players.append(player)
                waitlist.remove(player)

                player_found = True
                break

        if not player_found:
            break

    return seated_players
def remove_player_from_table(table, player_email, players):
    """
    Removes a player from a table and updates the table seat count.
    """

    for player in players:
        if player.email == player_email and player.currenttable == table.tablenum:
            player.currenttable = None
            player.activelyplaying = False

            if table.seatsfull > 0:
                table.seatsfull -= 1

            return True

    return False


def read_lines(filename):
    """Returns all lines from a text file."""
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


def write_lines(filename, lines):
    """Writes a list of lines to a text file."""
    with open(filename, "w") as file:
        for line in lines:
            file.write(line + "\n")


def save_player(player):
    """Saves a player to players.txt"""

    players = read_lines(PLAYERS_FILE)

    line = (
        f"{player.email}|"
        f"{player.name}|"
        f"{player.number}|"
        f"{player.currenttable}|"
        f"{player.activelyplaying}|"
        f"{player.password}"
    )

    players.append(line)
    write_lines(PLAYERS_FILE, players)


def load_players():
    """Loads all players from players.txt"""

    players = []

    for line in read_lines(PLAYERS_FILE):
        data = line.split("|")

        if len(data) == 6:
            players.append(data)

    return players

def save_waitlist(waitlist):
    """Saves the waitlist to waitlist.txt"""

    lines = []

    for player in waitlist:
        lines.append(
            f"{player.playerid}|"
            f"{player.tablewaitingfor}|"
            f"{player.jointime}"
        )

    write_lines(WAITLIST_FILE, lines)


def load_waitlist():
    """Loads the waitlist from waitlist.txt"""

    waitlist = []

    for line in read_lines(WAITLIST_FILE):
        data = line.split("|")

        if len(data) == 3:
            waitlist.append(data)

    return waitlist


def save_tables(tables):
    """Saves all tables to tables.txt"""

    lines = []

    for table in tables:
        lines.append(
            f"{table.tablenum}|"
            f"{table.seats}|"
            f"{table.seatsfull}|"
            f"{table.open}|"
            f"{table.image}"
        )

    write_lines(TABLES_FILE, lines)


def load_tables():
    """Loads all tables from tables.txt"""

    tables = []

    for line in read_lines(TABLES_FILE):
        data = line.split("|")

        if len(data) == 5:
            tables.append(data)

    return tables


def save_history(history):
    """Saves the game history to history.txt"""

    write_lines(HISTORY_FILE, history)

def load_history():
    """Loads the game history from history.txt"""

    return read_lines(HISTORY_FILE)