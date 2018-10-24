import sqlite3   #enable control of an sqlite database

def createUserTable(cur):
    ''' This function creates Users table in database with column names id, username, and password.'''
    command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def createStoriesTable(cur):
    ''' This function creates Stories table in database with column names id, title, body, and latestAddition.'''
    command = "CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL, latestAddition TEXT NOT NULL)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def createContributionsTable(cur):
    ''' This function creates Contributions table in database with column names id, user_id, and story_id.'''
    command = "CREATE TABLE IF NOT EXISTS contributions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, story_id INTEGER NOT NULL)" #build SQL stmt, save as string
    cur.execute(command) #run SQL statement

def createDatabase():
    ''' This function connect to the database and calls all the functions that create the tables in the database.'''
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    createUserTable(c)
    createStoriesTable(c)
    createContributionsTable(c)
    db.close() #close database
