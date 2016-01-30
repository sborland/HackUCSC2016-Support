from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml
from helper import *
import twilio.twiml
import sqlite3 as lite
import sys
 
 #suppress http request log
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)

ACCOUNT_SID = "ACc98c7be798532eb3bf9a428f5c152f64"
AUTH_TOKEN = "f177b7ab10a41be5f6fa9c82d5696f62"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

plang = ""
ploc = ""
pservice = []

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
    msg = request.values.get('Body', None)
    msg = msg.lower().split()
    user_number = request.values.get('From', None)

    parsed = ""
    for word in msg:
        parsed += word
    print parsed   

    print(checkCity(parsed))
    if(checkCity(parsed) == "true"):
        ploc = parsed
        return service()


    if(parsed.isdigit() == False):
        if parsed == "service":
            #check if user is subscribed or not
            return language()
        elif parsed == "unsubscribe":
            #unsubscribe
            return 	
        elif parsed == "english" or parsed == "spanish":
            plang = parsed
            return menu()
        elif parsed == "findvolunteer":
            #language
            return location()
        elif parsed == "getinfo":
            return
    else:
        for digit in parsed:
            print digit
            if digit == "1":
                pservice.append("shelter")
            elif digit == "2":
                pservice.append("food")
            elif digit == "3":
                pservice.append("law")
        #call to create user
        
        #print "preferred lang: " + plang
        #print "location: " + ploc
        #print "services : "
        #for x in pservice:
        #    print x
            else:
                resp = twilio.twiml.Response()
                resp.message("Invalid choice")
                return str(resp)		
        return finished()

@app.route("/finished", methods=['GET', 'POST'])
def finished():
    lang = "You have submitted a request for a volunteer!"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp)    


@app.route("/language", methods=['GET', 'POST'])
def language():
    lang = "What is your primary language?"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp)    

@app.route("/menu", methods=['GET', 'POST'])
def menu():
    choices = "Find volunteer \nGet info \nUnsubscribe"
    resp = twilio.twiml.Response()
    resp.message(choices)
    return str(resp)    
	
@app.route("/location", methods=['GET', 'POST'])
def location():
    loc = "What city do you live in?"
    resp = twilio.twiml.Response()
    resp.message(loc)
    return str(resp)    
	
@app.route("/service", methods=['GET', 'POST'])
def service():
    loc = "Which of the following do you need help with? \nText the number corresponding to your choice. \n1- Shelter \n2- Food \n3- Law"
    resp = twilio.twiml.Response()
    resp.message(loc)
    return str(resp)    
    


@app.route('/hello/')
def hello(name= 'Leslie'):
    return render_template('signup.html', name=name)


@app.route('/signup', methods = ['POST'])
def signup():
    print("HERE!")
    phone = request.form['phone']
    name = request.form['name']
    language = request.form['language']
    description = request.form['description']
    filename = phone
    f = open(filename,'a')
    f.write("phone\n")
    f.write( phone+ "\n")
    f.write("name\n")
    f.write( name+ "\n")
    f.write("language\n")
    f.write( language+ "\n")
    f.write("description\n")
    f.write( description+ "\n")
 

    f.close()
    print("The phone address is '" + phone+ "'")
    return hello()

if __name__ == "__main__":
    app.run(debug=True)