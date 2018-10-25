import sqlite3   #enable control of an sqlite database

def create_user_table(cur):
    ''' This function creates Users table in database with column names id, username, and password.'''
    command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def create_stories_table(cur):
    ''' This function creates Stories table in database with column names id, title, body, and latestAddition.'''
    command = "CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL, latestAddition TEXT NOT NULL, avg_rating INTEGER)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def create_contributions_table(cur):
    ''' This function creates Contributions table in database with column names id, user_id, and story_id.'''
    command = "CREATE TABLE IF NOT EXISTS contributions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, story_id INTEGER NOT NULL)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def create_ratings_table(cur):
    ''' This function creates Ratings table in database with column names id, user_id, story_id, and user_rating.'''
    command = "CREATE TABLE IF NOT EXISTS ratings (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, story_id INTEGER NOT NULL, user_rating INTEGER)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def create_database():
    ''' This function connect to the database and calls all the functions that create the tables in the database.'''
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    create_user_table(c)
    create_stories_table(c)
    create_contributions_table(c)
    create_ratings_table(c)
    db.close() #close database
