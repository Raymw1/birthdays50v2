from werkzeug.security import check_password_hash, generate_password_hash
from models import database

db = database.db

def createBirth(name, month, day, user_id):
  birth_id = db.execute("INSERT INTO birthdays (name, month, day, user_id) VALUES (?, ?, ?, ?);", name, month, day, user_id)
  return birth_id;

def getBirths(user_id):
  return db.execute("SELECT id, name, month, day FROM birthdays WHERE user_id = ?", user_id);
