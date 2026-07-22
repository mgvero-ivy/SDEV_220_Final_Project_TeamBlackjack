# models.py


class Table:
    def __init__(
        self,
        table_id,
        game_type,
        stakes,
        total_seats,
        players=None,
        waitlist=None
    ):
        self.table_id = table_id
        self.game_type = game_type
        self.stakes = stakes
        self.total_seats = total_seats

        # Use empty lists when no players or waitlist are provided
        self.players = players if players is not None else []
        # Convert the saved list into a Waitlist object
        self.waitlist = Waitlist(waitlist)

    def is_full(self):
        """
        Returns True when every seat is filled.
        """

        return len(self.players) >= self.total_seats

    def add_player(self, player_data):
        """
        Seats the player if space is available.
        Otherwise adds the player to the waiting list.
        """
        
        if self.is_full():
          self.waitlist.add_player(player_data)
          return "waitlisted"

        self.players.append(player_data)
        return "seated"

    def to_dict(self):
        """
        Converts the Table object into a dictionary
        that can be saved in data.txt.
        """

        return {
            "id": self.table_id,
            "game_type": self.game_type,
            "stakes": self.stakes,
            "total_seats": self.total_seats,
            "players": self.players,
            "waitlist": self.waitlist.to_list()
        }

    @classmethod
    def from_dict(cls, table_data):
        """
        Creates a Table object from a dictionary
        loaded from data.txt.
        """

        return cls(
            table_id=table_data["id"],
            game_type=table_data["game_type"],
            stakes=table_data["stakes"],
            total_seats=table_data["total_seats"],
            players=table_data.get("players", []),
            waitlist=table_data.get("waitlist", [])
        )

class User:
    def __init__(
        self,
        name,
        phone_number,
        player_id=None,
        current_table=None,
        actively_playing=False,
        password=None
    ):
        # Optional unique identifier for the player
        self.player_id = player_id

        # Information collected from the join form
        self.name = name
        self.phone_number = phone_number

        # Table and account information that may be used later
        self.current_table = current_table
        self.actively_playing = actively_playing
        self.password = password

    def to_dict(self):
        """
        Converts the User object into a dictionary
        that can be saved in data.txt.
        """

        return {
            "name": self.name,
            "phone_number": self.phone_number
        }


class Waitlist:
    def __init__(self, players=None):
        # Keep the waiting players in their original order
        self.players = players if players is not None else []

    def add_player(self, player_data):
        """
        Adds a player to the end of the waiting list.
        """

        self.players.append(player_data)

    def remove_player(self, player_index):
        """
        Removes a player using their position in the waiting list.
        Returns the removed player.
        """

        return self.players.pop(player_index)

    def get_next_player(self):
        """
        Removes and returns the first player in the waiting list.
        Returns None when the waiting list is empty.
        """

        if not self.players:
            return None

        return self.players.pop(0)

    def get_position(self, player_data):
        """
        Returns a player's numbered waiting-list position.
        """

        return self.players.index(player_data) + 1

    def is_empty(self):
        """
        Returns True when nobody is waiting.
        """

        return len(self.players) == 0

    def __len__(self):
        """
        Allows len(waitlist) to return the number waiting.
        """

        return len(self.players)

    def to_list(self):
        """
        Returns the regular list used by data.txt.
        """

        return self.players