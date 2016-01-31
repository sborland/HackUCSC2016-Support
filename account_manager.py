import sqlite3 as lite
import sys
import json
from Matching import *
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
    status = 0
    tagArray = []

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
    tagArray = []
    status = 0

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
        # i = 0
        while (arg != "EXIT"):
            arg = file.readline().rstrip()
            # print i
            Obj.tagArray.append(arg)
            # print arg
            # i=i+1
        deleteTagDup(Obj.tagArray)
        Obj.tagArray = filter(None, Obj.tagArray)
        Obj.tagArray.remove("EXIT")
        # print Obj.tagArray
        json_object = json.dumps(Obj.tagArray)
        arrayHelp = [(Obj.fName),(Obj.lName),(Obj.city),(Obj.state),(Obj.language),(Obj.phone), (Obj.email), (Obj.description),(Obj.status), json_object]
        cur.execute("SELECT phone FROM volunteers WHERE phone=?",(Obj.phone,))
        exists = cur.fetchone()
        if exists == None:
            cur.executemany("INSERT INTO volunteers VALUES(?,?,?,?,?,?,?,?,?,?)",[arrayHelp])
        Obj.tagArray = []
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
        # i = 0
        while (arg != "EXIT"):
            arg = file.readline().rstrip()
            # print i
            Obj.tagArray.append(arg)
            # print arg
            # i=i+1
        deleteTagDup(Obj.tagArray)
        Obj.tagArray = filter(None, Obj.tagArray)
        Obj.tagArray.remove("EXIT")
        # print Obj.tagArray
        json_object = json.dumps(Obj.tagArray)
        arrayHelp = [(Obj.phone),(Obj.volunteerID),(Obj.language),(Obj.fName),(Obj.lName),(Obj.city),(Obj.state),(Obj.description),json_object,(Obj.status)]
        cur.execute("SELECT z.Phone FROM clients z WHERE z.Phone=?",(Obj.phone,))
        exists = cur.fetchone()
        if exists == None:
            cur.executemany("INSERT INTO clients VALUES(?,?,?,?,?,?,?,?,?,?)",[arrayHelp])
        Obj.tagArray = []
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
    cur.execute("CREATE TABLE IF NOT EXISTS volunteers(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, Phone TEXT, Email TEXT, Description TEXT, Status INTEGER, Tags TEXT)")

    
    f = open(file)

    while True:
        nextLine = f.readline().rstrip()
        check = fileVolunteerCases(nextLine, f, volunteerObj, cur)
        if check == "break":
            break
    con.commit()
    # cur.execute("SELECT * FROM volunteers")
    # print cur.fetchall()
    # f.close()
    # con.close()

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
    # cur.execute("SELECT * FROM clients")
    # print cur.fetchall()
    f.close()
    con.close()

# Command line arguments
#script, filename1, filename2  = argv

# Initialization of volunteer object.
volunteerObj = volunteer(["title"])
clientObj = client(["title"])

# Other initializations
con = None
file = None

def clientVolunteerMatch(clientPhone):
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute("SELECT FirstName FROM clients WHERE Phone="+clientPhone)
    test1 = ''.join(cur.fetchone())
    cur.execute("SELECT Tags FROM clients WHERE Phone="+clientPhone)
    test2 = list(cur.fetchone())[0]
    cur.execute("SELECT Phone FROM volunteers")
    test3 = list(cur.fetchall())
    cur.execute("SELECT Tags FROM volunteers")
    test4 = cur.fetchall()
    test5 = []
    for i in test4:
        tmp = list(i)
        test5.append(tmp[0])
    volunteerPhone = list(matchVolunteer(test1, test2, test3, test5))[0]
    cur.execute("UPDATE clients SET VolunteerID =" + volunteerPhone + " WHERE Phone=" + clientPhone)
    cur.execute("SELECT VolunteerID FROM clients WHERE Phone="+clientPhone)
    volunteerID = ''.join(cur.fetchone())
    cur.execute("SELECT FirstName FROM clients WHERE Phone="+clientPhone)
    firstName = ''.join(cur.fetchone())
    cur.execute("SELECT Phone FROM clients WHERE Phone="+clientPhone)
    phone = ''.join(cur.fetchone())
    cur.execute("SELECT City FROM clients WHERE Phone="+clientPhone)
    city = ''.join(cur.fetchone())
    cur.execute("SELECT State FROM clients WHERE Phone="+clientPhone)
    state = ''.join(cur.fetchone())
    cur.execute("SELECT Description FROM clients WHERE Phone="+clientPhone)
    desc = ''.join(cur.fetchone())
    clientInfo = [volunteerID, firstName, phone, city, state, desc]
    return clientInfo
    # client volunteerID, firstname, phone, city, state, desc
    # returns phoneNum
    
def getItem(phone,category,person):
#phone - phone number
#category - city, state, desc etc
#person - either client or volunteer
#FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, Phone TEXT, Email TEXT, Description TEXT, Status INTEGER, Tags TEXT)
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute("SELECT " + category + " FROM "+person+ " WHERE Phone="+phone)
    string = ''.join(cur.fetchone())
    return string;
    
def deleteVolunteer(phone):
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute("DELETE FROM volunteers WHERE Phone="+phone)

def deleteClient(volunteerID):
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute("DELETE FROM clients WHERE VolunteerID="+volunteerID)

try:
    # Reading in the database files.
    con = lite.connect('service_database.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute("CREATE TABLE IF NOT EXISTS volunteers(FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Language TEXT, Phone TEXT, Email TEXT, Description TEXT, Status INTEGER, Tags TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS clients(Phone TEXT, VolunteerID TEXT, Language TEXT, FirstName TEXT, LastName TEXT, City TEXT, State TEXT, Description TEXT, Tags TEXT, Status INTEGER)")
    # print matchVolunteer(str(cur.execute("SELECT FirstName FROM clients WHERE FirstName='client'")),
    #                      str(cur.execute("SELECT Tags FROM clients WHERE FirstName='client'")),
    #                      str(cur.execute("SELECT FirstName FROM volunteers WHERE FirstName='volunteer'")),
    #                      str(cur.execute("SELECT Tags FROM volunteers WHERE FirstName='volunteer'")))

    # cur.execute("SELECT FirstName FROM clients WHERE FirstName='client'")
    # test1 = ''.join(cur.fetchone())
    # cur.execute("SELECT Tags FROM clients WHERE FirstName='client'")
    # test2 = list(cur.fetchone())[0]
    # cur.execute("SELECT FirstName FROM volunteers")
    # test3 = list(cur.fetchall())
    # cur.execute("SELECT Tags FROM volunteers")
    # test4 = cur.fetchall()
    # test5 = []
    # for i in test4:
    #     tmp = list(i)
    #     test5.append(tmp[0])
   # print list(matchVolunteer(test1, test2, test3, test5))[0]

    # testing
    # con.commit()
    #cur.execute("SELECT * FROM clients")
    #print cur.fetchall()
    
    #print getItem("18316005752","FirstName","clients")

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