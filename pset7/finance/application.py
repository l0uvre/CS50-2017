from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    #delete the unowned stock
    db.execute("DELETE FROM portfolio WHERE shares=0")

    # get stocks from the user
    stocks = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])

    # get user's current cashs
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
    total_cs = cash[0]["cash"]
    # update all users' stocks and calculate the user's total value currently
    for stock in stocks:
        symbol = stock["symbol"]
        name = stock["name"]
        shares = stock["shares"]
        price = lookup(symbol)["price"]
        total = price * int(shares)
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(price), total=usd(total), id=session["user_id"], symbol=symbol)
        total_cs += total

    # select the user
    stocks = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])
    # return the page for index after updating all info
    return render_template("index.html", total=usd(total_cs), stocks=stocks, cash=usd(cash[0]["cash"]))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # return the buy.hrml for GET
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        # ensure symbol is valid
        if (not request.form.get("symbol")) or (not stock):
            return apology("symbol you provided doesn't exist")


        # ensure the amount of shares is positive
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("shares must be a positive integer")
        except:
            return apology("shares must be a positive integer")


        # get the symbol's price
        price = lookup(request.form.get("symbol"))["price"]
        # get the user's cashs
        cashs = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        # calculate the money needed
        money = int(request.form.get("shares")) * price

        # ensure the user are able to buy the shares
        if cashs[0]["cash"] < money or not cashs:
            return apology("Not enough money")

        # insert the transactions into another table
        symbol_user = db.execute("SELECT * FROM portfolio WHERE id =:id AND symbol =:symbol", id=session["user_id"], symbol=stock["symbol"])
        # insert the shares info if the user didn't buy it previously
        if not symbol_user:
            db.execute("INSERT INTO portfolio (id, symbol, name, shares, price, total) VALUES(:id, :symbol, :name, :shares, :price, :total)", id=session["user_id"], symbol=stock["symbol"], name=stock["name"], shares=request.form.get("shares"), price=usd(price), total=usd(money))
        # otherwise update the info of shares
        else:
            #total money for shares of a specific symbol
            total = float(symbol_user[0]["total"].split('$')[1]) + int(request.form.get("shares")) * price
            db.execute("UPDATE portfolio SET shares=:shares WHERE id =:id AND symbol =:symbol", shares=symbol_user[0]["shares"]+shares, id=session["user_id"], symbol=stock["symbol"])
            db.execute("UPDATE portfolio SET total=:total WHERE id =:id AND symbol =:symbol", total=usd(total), id=session["user_id"], symbol=stock["symbol"])
        # update the user's cash
        db.execute("UPDATE users SET cash=cash - :purchase WHERE id=:id", purchase=money, id=session["user_id"])

        # update history table
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)", id=session["user_id"], symbol=stock["symbol"], shares=shares, price=usd(price))
        return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    histories = db.execute("SELECT * FROM history WHERE id=:id", id=session["user_id"])

    for history in histories:
        price_now = lookup(history["symbol"])["price"]
        db.execute("UPDATE history SET price_now=:price_now WHERE id=:id AND symbol=:symbol", price_now=usd(price_now), id=session["user_id"], symbol=history["symbol"])


    return render_template("history.html", histories=histories)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # allow user to open a html for quotes
    if request.method == "GET":
        return render_template("quote.html")
    # search from user's input form
    else:
        result = lookup(request.form.get("symbol"))
        # ensure the symbol is valid
        if not result:
            return apology("invalid symbol")
        else:
            return render_template("quoted.html", name=result["name"], symbol=result["symbol"], price=result["price"])


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

        #hashing the password from the form
        hashed = pwd_context.hash(request.form.get("password"))

        # query the database to register the user
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hashed)", username=request.form.get("username"), hashed=hashed)
        # ensure the unique username
        if not result:
            return apology("Sorry username already existed")

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # ensure the request mothod is GET
    if request.method == "GET":
        return render_template("sell.html")
    # deal with POST method
    else:
        # Get stock and shares from the POST
        stock = lookup(request.form.get("symbol"))

        # ensure shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("shares must be a positive integer")
        except ValueError:
            return apology("shares must be a positive integer")

        # ensure valid symbol
        if not stock:
            return apology("invalid symbol")


        # select the user's shares for the requested one
        symbol_user = db.execute("SELECT * FROM portfolio WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol=stock["symbol"])

        # ensure the user own that kind of stock
        if not symbol_user:
            return apology("Sorry, you don't own that stock")

        else:
            # ensure the user's shares are enough
            if symbol_user[0]["shares"] < shares:
                return apology("Sorry, you don't now that many shares")
            else:
                # shares remaining
                current_shares = symbol_user[0]["shares"] - shares
                # money got
                money_get = shares * stock["price"]
                # total value for the specific stock the user owned
                total = current_shares * stock["price"]
                #total money for shares of a specific symbol
                db.execute("UPDATE portfolio SET shares=:shares, total=:total WHERE id=:id AND symbol=:symbol", shares=current_shares, total=usd(total), id=session["user_id"], symbol=stock["symbol"])
                # update the user's cash
                db.execute("UPDATE users SET cash=cash + :got  WHERE id=:id", got=money_get, id=session["user_id"])

                # update history table
                db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)", id=session["user_id"], symbol=stock["symbol"], shares=-shares, price=usd(stock["price"]))

                return redirect(url_for("index"))
