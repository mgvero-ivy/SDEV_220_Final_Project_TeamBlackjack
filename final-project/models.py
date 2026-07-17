# models.py

class Table:
  def __init__(self, tablenum, seats, seatsfull, open):
    self.tablenum = tablenum
    self.seats = seats
    self.seatsfull = seatsfull
    self.open = open #Whether the table is open or closed

class User:
  def __init__(self, name, number, currenttable, activelyplaying, password):
    self.name = name
    self.number = number
    self.currenttable = currenttable
    self.activelyplaying = activelyplaying
    self.password = password

class Waitlist:
  def __init__(self, playerid, tablewaitingfor, jointime):
    self.playerid = playerid
    self.tablewaitingfor = tablewaitingfor
    self.jointime = jointime
