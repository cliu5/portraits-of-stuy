# Team WXYZ (Tina Wong, Raymond Wu, Jerry Ye, Ivan Zhang)
# SoftDev1 pd07
# P00 -- Da Art of Storytellin'
# 2018-10-17

import sqlite3   #enable control of an sqlite database
from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def landingPage():
    # TODO if logged in, show stories
    # not logged in
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

# a route that receives the login form and checks if the login information is correct
@app.route("/auth", methods=["POST"]) #assign fxn to route
def authenticate():
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = request.form['username']
    command = "SELECT username, password FROM users WHERE username={}".format(repr(user))
    c.execute(command)
    results = c.fetchall() # results contains the username and its corresponding password that matches the username from the form
    if results == []:
        flash("Username invalid. Try logging in again or registering for an account.")
        db.close()  #close database
        return render_template("login.html")
    for data in results:
        if data[1] != request.form['password']:
            db.close()  #close database
            flash("Password invalid. Try again.")
            return render_template('login.html')
        else:
            session["username"] = request.form["username"]
            db.close()  #close database
            return redirect(url_for('landingPage'))

# a route that removes the current user from the session and redirects the user back to the login page from home
@app.route('/logout')
def logout():
    session.pop('username') # ends session
    return redirect(url_for('landingPage'))

@app.route('/create_story')
def create_story():
    # title = request.form['title']
    # body = request.form['body']
    # latestAddition = body
    title = "WXYZ Story" # dummy data until page templating
    body = "hello there!" # dummy data until page templating
    latestAddition = body
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO stories (title, body, latestAddition) VALUES (\"{}\", \"{}\" , \"{}\")".format(title, body, latestAddition) )
    db.commit()
    db.close()


if __name__ == "__main__":
	app.debug = True  # TODO set to False when done!
	app.run()
