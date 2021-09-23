from functools import wraps
from flask import redirect, render_template, session

def apology(page, message, code=400, data=None):
  return render_template(page, error=message, data=data), code

def login_required(f):
  """
  Decorate routes to require login.

  https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
  """
  @wraps(f)
  def decorated_function(*args, **kwargs):
      if session.get("user_id") is None:
          return redirect("/")
      return f(*args, **kwargs)
  return decorated_function

def is_logged(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
      if session.get("user_id") is not None:
          return redirect("/birthdays")
      return f(*args, **kwargs)
  return decorated_function
