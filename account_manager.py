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

# Structure for the client object.
class client(object):
    def __init__(self, title):
        self.title = title
    phone = None
    volunteerID = None
    language = None
    fName = None
    lName = None
    city = None
    state = None
    description = None
    tagArray = [None]*101
    status = None

# Each of the cases for the respective groups.
def fileVolunteerCases(arg, file, Obj, cur):
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
        Obj.status = 0
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

def fileClientCases(arg, file, Obj, cur):
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
    elif arg == "volunteerID":
        Obj.volunteerID = ""
    elif arg == "description":
        Obj.description = file.readline().rstrip("\n")
    elif arg == "status":
        Obj.status = 0
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
        arrayHelp = [(Obj.phone),(Obj.volunteerID),(Obj.language),(Obj.fName),(Obj.lName),(Obj.city),(Obj.state),(Obj.description),json_object,(Obj.status)]
        cur.executemany("INSERT INTO clients VALUES(?,?,?,?,?,?,?,?,?,?)",[arrayHelp])
    elif arg == "":
        return "break"
    else:
        return

# Deletes any duplicates contained in the tagArray object within the volunteer object
def deleteTagDup(Obj):
    noDupes = []
    [noDupes.append(i) for i in Obj if not noDupes.count(i)]
    return noDupes

def insertVolunteer(file):

    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    
    # Creating both volunteer tables with the elements
    cur.execute("CREATE TABLE IF NOT EXISTS volunteers(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, PhoneNum TEXT, Email TEXT, Description TEXT, Status INTEGER, Tags TEXT)")

    
    f = open(file)

    while True:
        nextLine = f.readline().rstrip()
        check = fileVolunteerCases(nextLine, f, volunteerObj, cur)
        if check == "break":
            break
    con.commit()
    print "finished adding info"
    cur.execute("SELECT * FROM volunteers")
    print cur.fetchall()
    f.close()
    con.close()

def insertClient(file):
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str

    # Creating both volunteer tables with the elements
    cur.execute("CREATE TABLE IF NOT EXISTS clients(Phone TEXT, VolunteerID TEXT, Language TEXT, FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Description TEXT, Tags TEXT, Status INTEGER)")

    f = open(file)

    while True:
        nextLine = f.readline().rstrip()
        check = fileClientCases(nextLine, f, clientObj, cur)
        if check == "break":
            break
    con.commit()
    print "finished adding info"
    cur.execute("SELECT * FROM clients")
    print cur.fetchall()
    f.close()
    con.close()

# Command line arguments
#script, filename,  = argv

# Initialization of volunteer object.
volunteerObj = volunteer(["title"])
clientObj = client(["title"])

# Other initializations
con = None
file = None

try:
    # Reading in the database files.
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str

    #cur.execute("DROP TABLE IF EXISTS volunteers")
    #cur.execute("DROP TABLE IF EXISTS users")
    # Creating both volunteer and user tables with the elements
    #cur.execute("CREATE TABLE volunteers(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, PhoneNum TEXT, Email TEXT, Description TEXT, Status INTEGER, Tags TEXT)")
    #cur.execute("CREATE TABLE users(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, PhoneNum TEXT, VolunteerID TEXT, Description TEXT, Status INTEGER, Tags TEXT)")
    # Read the file and deal with each of the cases
    # If we hit the end of the file, then break.



    # testing
    # con.commit()
    # cur.execute("SELECT * FROM volunteers")
    # print cur.fetchall()

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