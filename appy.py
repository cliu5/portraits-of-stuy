# Team WXYZ (Tina Wong, Raymond Wu, Jerry Ye, Ivan Zhang)
# SoftDev1 pd07
# P00 -- Da Art of Storytellin'
# 2018-10-22

import sqlite3   #enable control of an sqlite database
from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom
import util.db_maker as db_maker

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def landing_page():
    '''This function renders the template for the landing page. If logged in, the landing page will display the title and latest addition of the stories that the user has contributed to.'''
    if 'username' in session:
        DB_FILE= "foo.db"
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username={}".format(repr(session["username"])))
        for data in c.fetchall():
            id_for_user = data[0]
            c.execute("SELECT story_id FROM contributions WHERE user_id={}".format(repr(id_for_user)))
            stories = []
            contributions = c.fetchall()
        for data in contributions:
            c.execute("SELECT title, latestAddition, id FROM stories WHERE id={}".format(data[0]))
            for story_info in c.fetchall():
                a_story = [story_info[0], story_info[1], story_info[2]]
                stories.append(a_story)
        db.close()
        return render_template("index.html", stories_contributed=stories)

    # not logged in
    return render_template("index.html")

@app.route("/login")
def login():
    '''This function renders the template for the login page.'''
    return render_template("login.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    '''This function receives requests about the user's username and password from the signup form and creates users by connecting and adding to the sqlite3 database. If the registration is successful, the sign up page will redirect to the login page. Otherwise, errors will flash on the signup page.'''
    user = request.form['username']
    password = request.form['password']
    confirmedPassword = request.form['confirmedPassword'] #passwords are not yet hashed
    if user == "":
        flash("Please make sure to enter a username!")
        return redirect(url_for('signup'))
    if password == "":
        flash("Please make sure to enter a password!")
        return redirect(url_for('signup'))
    if password != confirmedPassword: # checks to make sure two passwords entered are the same
        flash("Please make sure the passwords you enter are the same.")
        return redirect(url_for('signup'))
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE) # connecting to database
    c = db.cursor()
    command = "INSERT INTO users (username,password) VALUES ( \"{}\" , \"{}\")".format(user, password)
    try: #try will fail if username already exists in the database
        c.execute(command)
        db.commit()
        db.close()
        flash("Your account has been created")
        return redirect(url_for('login'))
    except:
        flash("Please enter another username. The one you entered is already in the database.")
        db.commit()
        db.close()
        return redirect(url_for('signup'))

@app.route("/signup")
def signup():
    '''This function renders the template for the sign up page, which includes the sign up form.'''
    return render_template("signup.html")

# a route that receives the login form and checks if the login information is correct
@app.route("/auth", methods=["POST"]) #assign fxn to route
def authenticate():
    '''This function accesses the existing database to authenticate the user by creating a session if it currently exists in the database. If username and password combination does not exist, redirects user to login page. '''
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
            return redirect(url_for('landing_page'))

# a route that removes the current user from the session and redirects the user back to the login page from home
@app.route('/logout')
def logout():
    '''This function pops the username from the session, logging the user out. Redirects user to landing page.'''
    session.pop('username') # ends session
    return redirect(url_for('landing_page'))

@app.route('/create_story')
def create_story():
    '''This function renders html form for create story if the user is logged in. If user is not logged in, redirects user to login page.'''
    if 'username' in session:
        return render_template("create_story.html")
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))

@app.route('/add_new_story', methods=["POST"])
def add_new_story():
    '''This function is the route that the create_story.html page directs the user to after submitting a prompt. If user is loggedin and query is complete, creates a new story'''
    # must be logged in to see this page
    if 'username' in session:
        pass
    # not logged in
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))

    title = request.form['title']
    body = request.form['body']
    latestAddition = body
    #print(title)
    #print(repr(body))
    if title == "":
        flash("Please make sure to enter a title!")
        return redirect(url_for('create_story'))
    if body == " ":
        flash("Please make sure to enter content for the story!")
        return redirect(url_for('create_story'))

    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO stories (title, body, latestAddition) VALUES (\"{}\", \"{}\" , \"{}\")".format(title, body, latestAddition) )
    c.execute("SELECT max(id) FROM stories")
    for data in c.fetchall():
        id_for_story = data[0]
        c.execute("SELECT id FROM users WHERE username={}".format(repr(session["username"])))
    for data in c.fetchall():
        id_for_user = data[0]
        c.execute("INSERT INTO contributions (user_id, story_id) VALUES (\"{}\", \"{}\")".format(id_for_user, id_for_story) )
    db.commit() # saves changes to database
    db.close() # closes database
    flash("Story created!")
    return redirect(url_for('landing_page'))

@app.route('/search', methods=["GET", "POST"])
def search():
    '''This function searches the database for stories and renders html page with search results'''
    # must be logged in to see this page
    if 'username' in session:
        pass
    # not logged in
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template("search.html")

    else: # POST method
        query = request.form['search-query']
        command = "SELECT id, title, latestAddition, avg_rating from stories WHERE title like '%{}%' OR latestAddition like '%{}%'".format(query, query)

        DB_FILE= "foo.db"
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute(command)
        results = c.fetchall()
        db.commit() # saves changes to database
        db.close() # closes database

        return render_template("search_results.html",
                               stories = results)

@app.route('/story/<story_id>', methods=["GET", "POST"])
def show_story(story_id):
    '''This function shows the story by ID and either displays a form to add the latest addition to a story or a form to rate the story.'''
    # must be logged in to see this page
    if 'username' in session:
        pass
    # not logged in
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))


    if request.method == 'GET':
        title = ""
        viewable_story = ""
        can_view_form = False

        DB_FILE= "foo.db"
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT title, body, latestAddition, avg_rating from stories WHERE id={}".format(story_id)
        c.execute(command)
        story = c.fetchone()

        # invalid story_id
        if story == None:
            flash("This story does not exist.")
            return redirect(url_for('landing_page'))

        # valid story_id ... story found in db
        title = story[0]
        body = story[1]
        latestAddition = story[2]
        avg_rating = story[3]

        command = "SELECT id from users WHERE username={}".format(repr(session["username"]))
        c.execute(command)
        user_id = c.fetchone()[0]

        command = "SELECT * from contributions WHERE user_id={} AND story_id={}".format(user_id,story_id)
        c.execute(command)
        result = c.fetchone()

        db.close()

        if result == None: # user has not interacted w/ story
            viewable_story = latestAddition
            can_view_form = True
        else:
            viewable_story = body
            can_view_form = False

        return render_template("story.html",
                               story_title = title,
                               viewable_story = viewable_story,
                               can_view_form = can_view_form,
                               avg_rating = avg_rating)
    else: # POST method

        DB_FILE= "foo.db"
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        if request.form.get('story_rating') != None:
            command = "SELECT id from users WHERE username={}".format(repr(session["username"]))
            c.execute(command)
            user_id = c.fetchone()[0] # get id of user

            rating = request.form['story_rating']
            command = "SELECT user_id FROM ratings WHERE user_id={} AND story_id={}".format(user_id, story_id)
            c.execute(command)
            if c.fetchone() == None: # if user has not rated the story before, add a row of data. else, update the row
                command = "INSERT INTO ratings (user_id, story_id, user_rating) VALUES ( \"{}\" , \"{}\", \"{}\" )".format(user_id, story_id, rating)
                c.execute(command)
            else:
                command = "UPDATE ratings SET user_rating=\"{}\" WHERE story_id={} AND user_id={}".format(rating, story_id, user_id )
                c.execute(command)

            command = "SELECT user_rating FROM ratings WHERE story_id={}".format(story_id)
            c.execute(command)

            # average the ratings
            sum = 0
            count = 0
            for data in c.fetchall():
                sum += data[0]
                count += 1
            avg = sum / count

            command = "UPDATE stories SET avg_rating=\"{}\" WHERE id={}".format( avg, story_id )
            c.execute(command)
            flash("Rating of story added!")

        else:
            command = "SELECT id from users WHERE username={}".format(repr(session["username"]))
            c.execute(command)
            user_id = c.fetchone()[0]

            command = "INSERT INTO contributions (user_id, story_id) VALUES ( \"{}\" , \"{}\")".format(user_id, story_id)
            c.execute(command)

            command = "SELECT body from stories WHERE id={}".format(story_id)
            c.execute(command)
            result = c.fetchone()
            body = result[0]

            latestAddition = request.form['addition']
            body += " " + request.form['addition']

            command = "UPDATE stories SET body=\"{}\", latestAddition=\"{}\" WHERE id={}".format( body, latestAddition, story_id )
            c.execute(command)

        db.commit()
        db.close()

        return redirect(url_for('show_story', story_id=story_id))  # refresh page

@app.route('/contribute')
def show_contributable_stories():

    # must be logged in to see this page
    if 'username' in session:
        pass
    # not logged in
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))

    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "SELECT id FROM users WHERE username={}".format(repr(session["username"]))
    c.execute(command)
    ID = c.fetchone()[0]

    command = "SELECT story_id FROM contributions WHERE user_id={}".format(ID)
    c.execute(command)
    contributed = c.fetchall()

    valueString = "("
    for tuple in contributed:
        valueString += str(tuple[0]) + ","
    valueString = valueString[::-1].replace(",", "", 1)[::-1] + ")"

    #print (valueString)
    command = "SELECT id, title, latestAddition from stories WHERE id NOT IN {}".format(valueString)
    #print (command)
    c.execute(command)
    stories = c.fetchall()

    db.close()
    return render_template("contribute.html", stories_contributed=stories)


if __name__ == "__main__":
    app.debug = True  # TODO set to False when done!
    db_maker.create_database()
    app.run()
