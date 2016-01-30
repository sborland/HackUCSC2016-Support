from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml
from helper import *
import twilio.twiml
import sqlite3 as lite
import sys
import json

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
def startup():
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
    

########html displays ####################
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/creators')
def creator():
	return render_template('creator.html')

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/signuppage')
def hello(name= 'Leslie'):
    return render_template('signup.html', name=name)


@app.route('/signup', methods = ['POST'])
def signup():
    #print("HERE!")
    phone = request.form['phone']
    fname = request.form['fname']
    lname = request.form['lname']
    city = request.form['city']
    state = request.form['state']
    email = request.form['email']
    fname = request.form['fname']
    language = request.form['language']
    description = request.form['description']
    filename = str("./volunteer/" + phone)
    f = open(filename,'a')
    f.write("fname\n")
    f.write( fname+ "\n")
    f.write("lname\n")
    f.write( lname+ "\n")
    f.write("city\n")
    f.write( city+ "\n")
    f.write("state\n")
    f.write( state+ "\n")
    f.write("language\n")
    f.write( language+ "\n")
    f.write("phone\n")
    f.write( phone+ "\n")
    f.write("email\n")
    f.write( email+ "\n")
    f.write("description\n")
    f.write( description+ "\n")
    choice_list = request.form.getlist("choices")
    f.write("tagArray")
    for x in choice_list:
        f.write(x + "\n")

    f.close()
    return index()

if __name__ == "__main__":
    app.run(debug=True)