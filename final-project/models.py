# models.py

class Tables:
  def __init__(self, tablenum, seats, seatsfull, open, image):
    self.tablenum = tablenum
    self.seats = seats
    self.seatsfull = seatsfull
    self.open = open
    self.image = image

class User:
  def __init__(self, email, name, number, currenttable, activelyplaying, password):
    self.email = email
    self.name = name
    self.number = number
    self.currenttable = currenttable
    self.activelyplaying = activelyplaying
    self.password = password

class Waitlist:
