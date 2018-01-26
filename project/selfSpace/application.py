import json
import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from helpers import *


## Usage: https://www.omdbapi.com/?apikey={your_key}5&t=pulp+fiction&y=1994
# configure application
app = Flask(__name__)
# configure database for this application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///space.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
"""
# custom filter
app.jinja_env.filters["usd"] = usd
"""

"""
define models used for flask_sqlalchemy and make it compatible with the database created before.
"""
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
    def __init__(self, name, password):
        self.name = name
        self.password = password

class Film(db.Model):
    __tablename__ = "films"
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    imdb = db.Column(db.Text, primary_key=True, nullable=False)
    image = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Film %r>' % self.title
    def __init__(self, user_id, title, year, imdb, image):
        self.user_id = user_id
        self.title = title
        self.year = year
        self.imdb = imdb
        self.image = image

class Diary(db.Model):
    __tablename__ = "diary"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    journal = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    films = Film.query.filter_by(user_id=session["user_id"]).all()

    return render_template("index.html", films=films)

@app.route("/addmovie", methods=["GET", "POST"])
@login_required
def addmovie():
    # return the buy.hrml for GET
    if request.method == "GET":
        return render_template("addmovie.html")
    else:
        title = request.form.get("title")
        year = request.form.get("year")
        data = get_imdbid(title, year)
        #print(data)
        # ensure the moive is valid
        if (not title) or (not year) or (data['Response'] == "False"):
            return apology("Movie you provided doesn't exist")
        # add to the database
        else:
            imdb = data['imdbID']
            image = data['Poster']
            film = Film(user_id=session["user_id"], title=title, year=year, imdb=imdb, image=image)
            db.session.add(film)
            db.session.commit()
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        user = User.query.filter_by(name=request.form.get("username")).first()
        # ensure username exists and password is correct
        if not pwd_context.verify(request.form.get("password"), user.password):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = user.id

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    if request.method == "GET":
        return render_template("record.html")
    else:
        result = request.form.get("input_board")
        # ensure the symbol is valid
        if not result:
            return apology("please complete your diary.")
        else:
            diary = Diary(user_id=session["user_id"], journal=result)
            db.session.add(diary)
            db.session.commit()
            diaries = Diary.query.filter_by(user_id=session["user_id"]).all()
            return render_template("board.html", diaries=diaries)


@app.route("/board")
@login_required
def board():
    diaries = Diary.query.filter_by(user_id=session["user_id"]).all()
    return render_template("board.html", diaries=diaries)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username")
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password")
        # ensure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match")

        username = request.form.get("username")
        password = request.form.get("password")
        #hashing the password from the form
        hashed = pwd_context.hash(password)


        # ensure the unique username
        user = User.query.filter_by(name=username).first()
        if user:
            return apology("Sorry username already existed")
        else:
            # query the database to register the user
            user = User(name=username, password=hashed)

        db.session.add(user)
        db.session.commit()
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
