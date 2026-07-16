import sqlite3

def get_connection():
    return sqlite3.connect("data.db")

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
