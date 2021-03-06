from services.birthdays import formatSharedBirthdays
from models.Birthday import createBirth, deleteBirth, deleteSharedBirth, getBirth, getBirths, getSharedBirth, shareBirth
from models.User import createUser, getUser, getUserByEmail, getUserByName
import os
from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session, Response
from models import database
from models.validators import checkBirth, checkUsers
from helpers import apology, apologyBirth, is_logged, login_required
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
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = database.db

@app.route("/")
@is_logged
def index():
  return render_template("index.html")


# ------------------------- RESGISTER --------------------------------
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
    return redirect("/birthdays")
  else:
    return render_template("register.html")

# -------------------------  LOGIN --------------------------------
@app.route("/login", methods=["GET", "POST"])
@is_logged
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    data = {"email": email}
    if not email or not password:
      return apology("login.html", "Please, fill all fields!", 400, data)
    user = getUserByEmail(email)
    if not user:
      return apology("login.html", "User not registered!", 400, data)
    user = user[0]
    if not check_password_hash(user["password"], password):
      return apology("login.html", "Invalid password!", 401 , data)
    session["user_id"] = user["id"]
    return redirect("/birthdays")
  else:
    return render_template("login.html")


# ------------------------- BIRTHDAYS --------------------------------
@app.route("/birthdays", methods=["GET", "POST"])
@login_required
def birthdays():
  if request.method == "POST":
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")
    data = {"name": name, "day": day, "month": month}
    birthdays = getBirths(session["user_id"])
    if not name or not day or not month:
      return apologyBirth("birthdays.html", "Please, fill all fields!", birthdays, 400, data)
    month = int(month)
    day = int(day)
    if not 12 >= month >= 1:
      return apologyBirth("birthdays.html", "Please, insert a valid month!", birthdays, 400, data)
    if (not 31 >= day >= 1) or (month in [4, 6, 9, 11] and day > 30) or (month == 2 and day > 29):
      return apologyBirth("birthdays.html", "Please, insert a valid day!", birthdays, 400, data)

    if checkBirth(name, session["user_id"]):
      return apologyBirth("birthdays.html", "Birthday already exists!", birthdays, 400, data)

    createBirth(name, month, day, session["user_id"])
    birthdays = getBirths(session["user_id"])
    return render_template("birthdays.html", birthdays=birthdays, success="Birthday added!")
  else:
    birthdays = getBirths(session["user_id"])
    return render_template("birthdays.html", birthdays=birthdays)


# ------------------------- REMOVE BIRTHDAY --------------------------------
@app.route("/remove-birthday", methods=["POST"])
@login_required
def removeBirthdays():
  id = request.form.get("id")
  birthdays = getBirths(session["user_id"])
  if not id:
    return apologyBirth("birthdays.html", "Please, choose a birthday!", birthdays, 400)
  birthday = getBirth(id)
  if not birthday:
    return apologyBirth("birthdays.html", "Please, insert a valid birthday!", birthdays, 400)
  birthday = birthday[0]
  if birthday["user_id"] != session["user_id"]:
    return apologyBirth("birthdays.html", "Please, insert a birthday from your list!", birthdays, 400)
  deleteBirth(id)
  birthdays = getBirths(session["user_id"])
  return render_template("birthdays.html", birthdays=birthdays, success="Birthday removed!")


# ------------------------- SHARE BIRTHDAYS --------------------------------
@app.route("/share", methods=["GET", "POST"])
@login_required
def share():
  if request.method == "POST":
    birthdays = getBirths(session["user_id"])
    births = request.form.getlist("birthday")
    username = request.form.get("username")
    data = {"username": username}
    if not births:
      return apologyBirth("share.html", "Please, insert at least one birthday!", birthdays, 400, data)
    if not username:
      return apologyBirth("share.html", "Please, insert an username!", birthdays, 400, data)
    receiver = getUserByName(username)
    if not receiver:
      return apologyBirth("share.html", "Please, insert a valid username!", birthdays, 400, data)
    receiver = receiver[0]["id"]
    if receiver == session["user_id"]:
      return apologyBirth("share.html", "Please, insert another username!", birthdays, 400, data)
    for birth in births:
      shareBirth(session["user_id"], receiver, int(birth))
    return render_template("share.html", success="Birthday shared!", birthdays=birthdays)
  else:
    birthdays = getBirths(session["user_id"])
    return render_template("share.html", birthdays=birthdays)

# ------------------------- RECEIVE BIRTHDAYS --------------------------------
@app.route("/receive")
@login_required
def receive():
  users = formatSharedBirthdays(session["user_id"])
  return render_template("receive.html", users=users)


# ------------------------- REMOVE SHARED BIRTHDAY --------------------------------
@app.route("/remove-shared", methods=["POST"])
@login_required
def removeShared():
  id = request.form.get("id")
  users = formatSharedBirthdays(session["user_id"])
  if not id:
    return render_template("receive.html", error="Please, choose a birthday!", users=users), 400
  birthday = getSharedBirth(id)
  if not birthday:
    return render_template("receive.html", error="Please, insert a valid birthday!", users=users), 400
  birthday = birthday[0]
  if birthday["receiver_id"] != session["user_id"]:
    return render_template("receive.html", error="Please, insert a birthday from your list!", users=users), 400
  deleteSharedBirth(id)
  users = formatSharedBirthdays(session["user_id"])
  return render_template("receive.html", users=users, success="Birthday removed!")


# -------------------------  LOGOUT --------------------------------
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

