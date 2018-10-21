### portraits-of-stuy
### Team WXYZ (Tina Wong, Raymond Wu, Jerry Ye, Ivan Zhang)
---

## Usage

**System requirements**: You will need Python 3 as well as SQLite 3 on your system. If, in your terminal, running `$ python3` invokes the Python 3 interpreter, and running `$ sqlite3` opens the SQLite 3 shell, you are good to go.

First, clone this repository:
```
$ git clone git@github.com:ivzhang1/portraits-of-stuy.git
```

Next, change your directory to go into your local copy of the repository:
```
$ cd portraits-of-stuy
```

Activate your virtual environment. If you do not have one set up, you may create one in the current working directory, and activate it like so:
```
$ python3 -m venv dc
$ . dc/bin/activate
```

In your virtual environment, install the following pip packages:
```
(dc) $ pip3 install wheel
(dc) $ pip3 install flask
```

Now, run the python file to start the Flask server:
```
(dc) $ python appy.py
```

Finally, open your web browser and open `localhost:5000`.

To exit your virtual environment, run the command `$ deactivate`.