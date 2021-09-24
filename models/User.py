from werkzeug.security import check_password_hash, generate_password_hash
from models import database

db = database.db

def createUser(email, username, password):
  password = generate_password_hash(password)
  user_id = db.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?);", email, username, password)
  return user_id;

def getUser(id):
  return db.execute("SELECT * FROM users WHERE id = ?", id);

def getUserByEmail(email):
  return db.execute("SELECT * FROM users WHERE email = ?", email);

def getUserByName(name):
  return db.execute("SELECT * FROM users WHERE username = ?", name);
