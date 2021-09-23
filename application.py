from models.User import createUser
import os
from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session, Response
from models import database
from models.validators import checkUsers
from helpers import apology
from flask_session import Session

app = Flask(__name__, static_url_path='', static_folder='static')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = database.db

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    passwordRepeat = request.form.get("passwordRepeat")
    if not email or not username or not password or not passwordRepeat:
      return apology("register.html", "Please, fill all fields!", 400, {"email": email, "username": username})
    if password != passwordRepeat:
      return apology("register.html", "Passwords didn't match!", 400, {"email": email, "username": username})
    if checkUsers(email, username):
      return apology("register.html", "User already registered!", 400, {"email": email, "username": username})
    user_id = createUser(email, username, password);
    session["user_id"] = user_id
    return render_template("index.html")
  else:
    return render_template("register.html")

@app.route("/login")
def login():
  return render_template("login.html")