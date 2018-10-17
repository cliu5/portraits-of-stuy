# Team WXYZ (Tina Wong, Raymond Wu, Jerry Ye, Ivan Zhang)
# SoftDev1 pd07
# P00 -- Da Art of Storytellin'
# 2018-10-17

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def landingPage():
    # TODO if logged in, show stories
    # not logged in
    return render_template("index.html")

if __name__ == "__main__":
	app.debug = True  # TODO set to False when done!
	app.run()
