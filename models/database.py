from cs50 import SQL
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, email TEXT NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, PRIMARY KEY(id));")
db.execute("""CREATE TABLE IF NOT EXISTS birthdays (id INTEGER, name TEXT NOT NULL, month INTEGER NOT NULL, day INTEGER NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);""")
db.execute("""CREATE TABLE IF NOT EXISTS shared (id INTEGER, sender_id INTEGER NOT NULL, receiver_id INTEGER NOT NULL, birthday_id INTEGER NOT NULL, PRIMARY KEY(id), FOREIGN KEY(sender_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(receiver_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(birthday_id) REFERENCES birthdays(id) ON DELETE CASCADE);""")
db.execute("PRAGMA foreign_keys = ON")

