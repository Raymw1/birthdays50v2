import os
from flask import Flask, redirect, render_template, request, session, Response
from flask_session import Session

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route("/")
def index():
  return render_template("index.html")