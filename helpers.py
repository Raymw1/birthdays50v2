from flask import render_template
def apology(page, message, code=400, data=None):
  return render_template(page, error=message, data=data), code