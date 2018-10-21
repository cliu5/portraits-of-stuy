import sqlite3   #enable control of an sqlite database

def createUserTable(cur):
    command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)"
    cur.execute(command)

def createStoriesTable(cur):
    command = "CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL, latestAddition TEXT NOT NULL)"
    cur.execute(command)

def createContributionsTable(cur):
    command = "CREATE TABLE IF NOT EXISTS contributions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, story_id INTEGER NOT NULL)"
    cur.execute(command)

def createDatabase():
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    createUserTable(c)
    createStoriesTable(c)
    createContributionsTable(c)
    db.close()  #close database
