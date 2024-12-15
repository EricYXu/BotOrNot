import os
import random
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
import requests

# Configuring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Connects to database
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

""" Home """
@app.route('/')
def index():
    format = random.randint(1,3)
    conn = get_db_connection()
    humanIndices = conn.execute('SELECT COUNT(*) AS text_count FROM humanText').fetchone()['text_count']
    botIndices = conn.execute('SELECT COUNT(*) AS text_count FROM botText').fetchone()['text_count']
    conn.close()

    if format == 1:
        """ Human Human """
        index1 = random.randint(1,humanIndices) 
        index2 = random.randint(1,humanIndices)
        while index2 == index1:
            index2 = random.randint(1,humanIndices)

        # Grabs text
        text1 = conn.execute('SELECT * FROM humanText WHERE id = ?',index1).fetchone()
        text2 = conn.execute('SELECT * FROM humanText WHERE id = ?',index2).fetchone()

    elif format == 2:
        """ Human Bot """
        index1 = random.randint(1,humanIndices) 
        index2 = random.randint(1,botIndices)

        # Grabs text
        text1 = conn.execute('SELECT * FROM humanText WHERE id = ?',index1).fetchone()
        text2 = conn.execute('SELECT * FROM botText WHERE id = ?',index2).fetchone()


    else:
        """ Bot Bot """
        index1 = random.randint(1,humanIndices) 
        index2 = random.randint(1,botIndices)
        while index2 == index1:
            index2 = random.randint(1,botIndices)

        # Grabs text
        text1 = conn.execute('SELECT * FROM botText WHERE id = ?',index1).fetchone()
        text2 = conn.execute('SELECT * FROM botText WHERE id = ?',index2).fetchone()

    # TODO: Later, try to generate some elo system for players and text blocks --> make some leaderboard
    return render_template('home.html',text1=text1, text2=text2)

@app.route('/login', methods=["GET", "POST"])
def login():
    """ Logs in user """
    session.clear()

    if request.method == "POST":
        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        conn.close()
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('Successfully logged in!')
        return redirect("/landing")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Checks validity of fields
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("Password and confirmation must match", 400)
        try:
            # Adds new user to the same database used for login
            conn = sqlite3.connect('site.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            # Returns error if username is already taken
            return apology("Username already taken", 400)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/landing", methods=["GET", "POST"])
def landing():
    """Sends logged-in user to landing dashboard"""

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Query database for the logged-in user's information
    conn = sqlite3.connect("site.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return render_template("landing.html", data=user)

# TODO: Using POST route to allow users to submit their own prompts, responses, based on elo --> request/test
@app.route("/")


@app.route("/logout")
def logout():
    """ Logs user out """
    session.clear()
    
    return redirect("/")

if __name__ == '__main__':
    app.run(app, debug=True)