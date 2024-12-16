import os
from flask import Flask, request, redirect, render_template, session, flash
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit
import random

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
    return render_template('home.html')

""" Tutorial """
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

""" Game """
@app.route('/game', methods=["GET", "POST"])
def game():
    if "user_id" not in session:
        flash('Please create an account first.')
        return redirect("/")

    # Gets user information
    user_id = session["user_id"]
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    # Formats the game
    format = random.randint(1,2)
    promptIndices = conn.execute('SELECT COUNT(*) AS prompt_count FROM prompts').fetchone()['prompt_count']
    promptIndex = random.randint(1,promptIndices)
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?',(promptIndex,)).fetchone()

    if format == 1:
        """ Bot Human """
        text1 = conn.execute('SELECT * FROM botText WHERE id = ?',(promptIndex,)).fetchone()
        text2 = conn.execute('SELECT * FROM humanText WHERE id = ?',(promptIndex,)).fetchone()

    else:
        """ Human Bot """
        text1 = conn.execute('SELECT * FROM humanText WHERE id = ?',(promptIndex,)).fetchone()
        text2 = conn.execute('SELECT * FROM botText WHERE id = ?',(promptIndex,)).fetchone()

    # Closes database
    conn.close()

    # TODO: Game Logic
    if request.method == 'POST':
        response1 = request.form.get('response1')
        response2 = request.form.get('response2')
        numberCorrect = 0

        if format == 1:
            if response1 == "bot1" and response2 == "human2":
                numberCorrect = 2
            elif response1 == "human1" and response2 == "bot2":
                numberCorrect = 0
            else:
                numberCorrect = 1
        else:
            if response1 == "human1" and response2 == "bot2":
                numberCorrect = 2
            elif response1 == "bot1" and response2 == "human2":
                numberCorrect = 0
            else:
                numberCorrect = 1

        # TODO: Find a way to alter the ELO of prompts and texts
        

        # TODO: Find a way to alter the user ELO after a successful or unsuccessful guess


        

    # TODO: Later, try to generate some elo system for players and text blocks --> make some leaderboard
    return render_template('game.html',text1=text1, text2=text2, prompt=prompt,user=user)

""" Login """
@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        conn.close()

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print("Yay!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash('Successfully logged in!')
        return redirect("/game")
    else:
        return render_template("login.html")

""" Register """
@app.route("/register", methods=["GET", "POST"])
def register():
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

""" Landing """
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

""" Logout """
@app.route("/logout")
def logout():
    """ Logs user out """
    session.clear()
    flash('Successfully logged out.')
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)