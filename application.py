from models.User import createUser, getUser
import os
from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session, Response
from models import database
from models.validators import checkUsers
from helpers import apology, is_logged, login_required
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

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
@is_logged
def index():
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
@is_logged
def register():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    passwordRepeat = request.form.get("passwordRepeat")
    data = {"email": email, "username": username}
    if not email or not username or not password or not passwordRepeat:
      return apology("register.html", "Please, fill all fields!", 400, data)
    if password != passwordRepeat:
      return apology("register.html", "Passwords didn't match!", 400, data)
    if checkUsers(email, username):
      return apology("register.html", "User already registered!", 400, data)
    user_id = createUser(email, username, password);
    session["user_id"] = user_id
    return render_template("birthdays.html")
  else:
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
@is_logged
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    data = {"email": email}
    user = getUser(email)[0]
    if not email or not password:
      return apology("login.html", "Please, fill all fields!", 400, data)
    if not user:
      return apology("login.html", "User not registered!", 400, data)
    if not check_password_hash(user["password"], password):
      return apology("login.html", "Invalid password!", 401 , data)
    session["user_id"] = user["id"]
    return render_template("birthdays.html")
  else:
    return render_template("login.html")

@app.route("/birthdays", methods=["GET", "POST"])
@login_required
def birthdays():
  if request.method == "POST":
    return render_template("birthdays.html")
  else:
    return render_template("birthdays.html")