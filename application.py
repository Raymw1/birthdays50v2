import os
from flask import Flask, redirect, render_template, request, session, Response
from models import database
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

@app.route("/register")
def register():
  return render_template("register.html")

@app.route("/login")
def login():
  return render_template("login.html")