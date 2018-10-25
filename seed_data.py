DB_FILE= "foo.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
userNames = ['Ivan', 'Jerry', 'Raymond', 'Tina', 'Mr. Brown']
passwords = [ '01', '02', '03', '04', '100']
commands = []
i = 0
while i < len(userNames):
    commands.append("INSERT INTO users (username,password) VALUES ( \"{}\" , \"{}\")".format(userNames[i], passwords[i]))
    print "Created User " + userName[i] + " with Password " + passwords[i]
for command in commands:
    c.execute(command)
