import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

def createUserTable(cur):
    command = "CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    cur.execute(command)
def createStoriesTable(cur):
    command = "CREATE TABLE stories(id INTEGER PRIMARY KEY, title TEXT, body TEXT, latestAddition TEXT)"
    cur.execute(command)
def main():
    DB_FILE= "foo.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    createUserTable(c)
    createStoriesTable(c)
    db.close()  #close database
main()
