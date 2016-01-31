#Admin file
#
#
import sqlite3 as lite
import sys
import json
from Matching import *
from array import array
from sys import argv
import glob,os

path = os.getcwd()
newPath = path+"/volunteer"
files = [f for f in os.listdir('./volunteer') if os.path.isfile(f)]
print files
for f in files:
    print f
    file = open(os.path.join(newPath, f), "r")    
    file.readline()
    print "Volunteer Name:"
    print file.readline()
    file.readline()
    print file.readline()
    file.readline()
    print "City:"
    file.readline()
    print "State:"
    file.readline()
    print file.readline()
    file.readline()
    print "Language:"
    print file.readline()
    file.readline()
    print "Phone:"
    print file.readline()
    file.readline()
    print "Email:"
    print file.readline()
    file.readline()
    print "Description:"
    print file.readline()
    file.readline()
    print "Tags"
    tag = file.readline()    
    while (tag != "EXIT"): 
         print tag
         tag = file.readline()
    check = raw_input('Type whether accept or decline to input:\n')
    if (check=="accept"):
        print "accept"
        filename = str("./volunteer/" + f)
        insertVolunteer(filename)
        os.remove(filename)
    elif (check=="decline"):
        print "decline"
        os.remove(filename)
    else:
        print "Unknown command. Skipping form to next form."
    print "\n"
    
print "Admin Form Completed"