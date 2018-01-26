import urllib.request
import urllib.parse
import json
import os

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

"""
by omdbapi, get the film data related to the query
"""
def get_imdbid(title, year):
    url = "https://www.omdbapi.com/?apikey={2}&t={0}&y={1}".format(urllib.parse.quote(title), year, os.environ.get("API_KEY"))
    try:
        data = json.load(urllib.request.urlopen(url))
        return data
    except:
        pass


