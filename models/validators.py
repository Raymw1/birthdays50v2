from models import database

db = database.db

def checkUsers(email, username):
  user = db.execute("SELECT id FROM users WHERE email = ? OR username = ?", email, username)
  if user:
    return 1
  return 0