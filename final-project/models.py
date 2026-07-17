# models.py

class Table:
  def __init__(self, tablenum, seats, seatsfull, open):
    self.tablenum = tablenum #Number to identify the table
    self.seats = seats #Total numbers of seats
    self.seatsfull = seatsfull #Number of seats full
    self.open = open #Whether the table is open or closed

class User:
  def __init__(self, UID, name, phonenumber, currenttable, activelyplaying, password):
    self.UID = UID #User ID
    self.name = name #Name of user
    self.phonenumber = phonenumber #Phone number used to identify user
    self.currenttable = currenttable #What table the user is currently at
    self.activelyplaying = activelyplaying #Whether the player is actively playing
    self.password = password #Password for the user

class Waitlist:
  def __init__(self, playerid, tablewaitingfor, jointime):
    self.playerid = playerid #Player UID
    self.tablewaitingfor = tablewaitingfor #Which table the player is waiting for
    self.jointime = jointime #What time the user joined the waitlist
