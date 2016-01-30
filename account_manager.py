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
    tagArray = [None]*101


# Each of the cases for lines.
def fileCases(arg, file, Obj, cur):
    #print(arg)
    if arg == "phone":
        Obj.phone = file.readline().rstrip()
        #print Obj.phone
        #print type(Obj.phone)
        return "go"
    elif arg == "email":
        Obj.email = file.readline().rstrip()
        #print type(Obj.email)
        return "go"
    elif arg == "client":
        Obj.client = file.readline().rstrip()
        #print type(Obj.client)
        return "go"
    elif arg == "language":
        Obj.language = file.readline().rstrip()
        #print type(Obj.language)
        return "go"
    elif arg == "tagArray":
        i = -1
        while (arg != "EXIT"):
            arg = file.readline().rstrip()
            i=i+1
            #print i
            Obj.tagArray[i] = arg
            #print type(Obj.tagArray[i])
        #deleteTagDup(Obj)
        arrayHelp = [str(volunteerObj.phone), str(volunteerObj.email), str(volunteerObj.client), str(volunteerObj.language), "z"]
        print arrayHelp
        cur.executemany("INSERT INTO volunteers VALUES(?,?,?,?,?)",[arrayHelp])
        return "stop"
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

# Inserts the multiple instances of the tag into the table.
# def insertTags(Obj, cur):
#     cur.executemany("UPDATE ")
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
    cur.execute("CREATE TABLE  volunteers(PhoneNum TEXT, Email TEXT, Client TEXT, Language TEXT, Tags TEXT)")

    # Read the file and deal with each of the cases
    # If we hit the end of the file, then break.

    while True:
        nextLine = file.readline().rstrip()
        check = fileCases(nextLine, file, volunteerObj, cur)
        if check == "break":
            break


    con.commit()
        #testing
    cur.execute("SELECT * FROM volunteers")
    print unicode(str(cur.fetchall()))

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