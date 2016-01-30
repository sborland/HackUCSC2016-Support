import sqlite3 as lite
import sys
import json
from array import array
from sys import argv


# Structure for the volunteer object.
class volunteer(object):
    def __init__(self, title):
        self.title = title
    fName = None
    lName = None
    city = None
    state = None
    language = None
    phone = None
    email = None
    description = None
    status = None
    tagArray = [None]*101

# Each of the cases for lines.
def fileCases(arg, file, Obj, cur):
    if arg == "fName":
        Obj.fName = file.readline().rstrip()
    elif arg == "lName":
        Obj.lName = file.readline().rstrip()
    elif arg == "city":
        Obj.city = file.readline().rstrip()
    elif arg == "state":
        Obj.state = file.readline().rstrip()
    elif arg == "language":
        Obj.language = file.readline().rstrip()
    elif arg == "phone":
        Obj.phone = file.readline().rstrip()
    elif arg == "email":
        Obj.email = file.readline().rstrip()
    elif arg == "description":
        Obj.description = file.readline().rstrip("\n")
    elif arg == "status":
        Obj.status = file.readline().rstrip()
    elif arg == "tagArray":
        i = -1
        while (arg != "EXIT"):
            arg = file.readline().rstrip()
            i=i+1
            Obj.tagArray[i] = arg
        deleteTagDup(Obj.tagArray)
        Obj.tagArray = filter(None, Obj.tagArray)
        Obj.tagArray.remove("EXIT")
        json_object = json.dumps(Obj.tagArray)
        arrayHelp = [(Obj.fName),(Obj.lName),(Obj.city),(Obj.state),(Obj.language),(Obj.phone), (Obj.email), (Obj.description),(Obj.status), json_object]
        cur.executemany("INSERT INTO volunteers VALUES(?,?,?,?,?,?,?,?,?,?)",[arrayHelp])
        resetObj(Obj)
    elif arg == "":
        return "break"
    else:
        return



# Resets the object after it's been inserted into the table.
def resetObj(Obj):
    Obj.phone = None
    Obj.email = None
    Obj.client = None
    Obj.language = None
    Obj.tagArray = [None]*50

# Deletes any duplicates contained in the tagArray object within the volunteer object
def deleteTagDup(Obj):
    noDupes = []
    [noDupes.append(i) for i in Obj if not noDupes.count(i)]
    return noDupes

# Command line arguments
script, filename = argv

# Initialization of volunteer object.
volunteerObj = volunteer(["title"])

# Other initializations
con = None
file = None

try:
    # Reading in the database file.
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    file = open(filename)

    cur.execute("DROP TABLE IF EXISTS volunteers")
    # Creating the table with the elements
    cur.execute("CREATE TABLE  volunteers(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, PhoneNum TEXT, Email TEXT, Description TEXT, Status TEXT, Tags TEXT)")

    # Read the file and deal with each of the cases
    # If we hit the end of the file, then break.

    while True:
        nextLine = file.readline().rstrip()
        check = fileCases(nextLine, file, volunteerObj, cur)
        if check == "break":
            break


    #testing
    con.commit()
    cur.execute("SELECT * FROM volunteers")
    print cur.fetchall()

# Error handling: prints out error location
except lite.Error, e:
    if con:
        con.rollback()
    print "Error %s:" % e.args[0]
    sys.exit(1)

# Closes connection and file.
finally:
    if con:
        con.close()
        file.close()