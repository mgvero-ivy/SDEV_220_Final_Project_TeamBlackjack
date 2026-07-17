# models.py

class Table:
  def __init__(self, tabl_enum, seats, seats_full, open):
    self.table_num = table_num #Number to identify the table
    self.seats = seats #Total numbers of seats
    self.seats_full = seats_full #Number of seats full
    self.open = open #Whether the table is open or closed

class User:
  def __init__(self, player_id, name, phone_number, current_table, actively_playing, password):
    self.player_id = player_id #User ID
    self.name = name #Name of user
    self.phone_number = phone_number #Phone number used to identify user
    self.current_table = current_table #What table the user is currently at
    self.actively_playing = actively_playing #Whether the player is actively playing
    self.password = password #Password for the user

class Waitlist:
  def __init__(self, player_id, table_waiting_for, join_time):
    self.player_id = player_id #Player UID
    self.table_waiting_for = table_waiting_for #Which table the player is waiting for
    self.join_time = join_time #What time the user joined the waitlist
