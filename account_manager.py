import sqlite3 as lite
import sys
from array import array
from sys import argv

script, filename = argv

try:

    con = lite.connect('serviceDatabase.db')