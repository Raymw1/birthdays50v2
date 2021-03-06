from werkzeug.security import check_password_hash, generate_password_hash
from models import database

db = database.db

def getBirth(id):
  return db.execute("SELECT * FROM birthdays WHERE id = ?", id)

def getBirths(user_id):
  return db.execute("SELECT id, name, month, day FROM birthdays WHERE user_id = ?", user_id)

def createBirth(name, month, day, user_id):
  birth_id = db.execute("INSERT INTO birthdays (name, month, day, user_id) VALUES (?, ?, ?, ?);", name, month, day, user_id)
  return birth_id

def deleteBirth(id):
  return db.execute("DELETE FROM birthdays WHERE id = ?", id)

def shareBirth(sender, receiver, id):
  if not checkIfBirthExists(sender, id):
    return db.execute("INSERT INTO shared (sender_id, receiver_id, birthday_id) VALUES (?, ?, ?)", sender, receiver, id)
  return

def checkIfBirthExists(sender, id):
  return db.execute("SELECT * FROM shared WHERE sender_id = ? AND birthday_id = ?", sender, id)

def getSharedBirth(id):
  return db.execute("SELECT * FROM shared WHERE id = ?", id)

def getSharedBirths(receiver_id):
  return db.execute("SELECT * FROM shared WHERE receiver_id = ?", receiver_id)

def deleteSharedBirth(id):
  return db.execute("DELETE FROM shared WHERE id = ?", id)
