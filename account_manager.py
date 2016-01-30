import sqlite3 as lite
import sys
from array import array
from sys import argv

# Structure for the volunteer object.
class volunteer(object):
    def __init__(self, title):
        self.title = title
    phone = None
    email = None
    client = None
    language = None
    tagArray = [None]*50


# Each of the cases for lines.
def fileCases(arg, file, Obj):
    if arg == "phone":
        Obj.phone = file.readline()
    elif arg == "email":
        Obj.email = file.readline()
    elif arg == "client":
        Obj.client = file.readline()
    elif arg == "language":
        Obj.language = file.readline()
    elif arg == "tagArray":
        i = -1
        while (arg != "\n"):
            Obj.tagArray[++i] = file.readline()
    else:
        return "break"


# Command line arguments
script, filename = argv

# Initialization of volunteer object.
volunteerObj = volunteer(["title"])

try:
    # Reading in the database file.
    con = lite.connect('service_database.db')
    cur = con.cursor()
    file = open(filename)

    # Creating the table with the elements
    cur.execute('''CREATE TABLE  volunteers(PhoneNum TEXT, Email TEXT, Client TEXT, Language TEXT, Tags TEXT)''')

    # Read the file and deal with each of the cases
    # If we hit the end of the file, then break.

    while True:
        nextLine = file.readline()

        if(fileCases(nextLine, file, volunteerObj) == "break"):
            break

