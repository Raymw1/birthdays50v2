from models import database

db = database.db

def checkUsers(email, username):
  user = db.execute("SELECT id FROM users WHERE email = ? OR username = ?", email, username)
  if user:
    return 1
  return 0

def checkBirth(name, user_id):
  birth = db.execute("SELECT id FROM birthdays WHERE name = ? AND user_id = ?", name, user_id)
  if birth:
    return 1
  return 0
