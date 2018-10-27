import sqlite3

DB_FILE= "foo.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
userNames = ['Ivan', 'Jerry', 'Raymond', 'Tina', 'Mr. Brown']
passwords = [ '01', '02', '03', '04', '100']
commands = []
i = 0
while i < len(userNames):
    commands.append("INSERT INTO users (username,password) VALUES ( \"{}\" , \"{}\")".format(userNames[i], passwords[i]))
    print ("Created User " + userNames[i] + " with Password " + passwords[i])
    i += 1
stories = {"Story1":"This is a great story!","Story2":"This is a bad story!","Story3":"This is a terrible story!","Story4":"This is a amazing story!","Story5":"This is a fantastic story!", }
i = 0
for title in stories:
    commands.append("INSERT INTO stories (title, body, latestAddition) VALUES (\"{}\", \"{}\" , \"{}\")".format(title, stories[title], stories[title]))
    commands.append("INSERT INTO contributions (user_id, story_id) VALUES (\"{}\", \"{}\")".format(i,i))
    i += 1
for command in commands:
    c.execute(command)
db.commit()
db.close()
