from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml
from helper import *
import twilio.twiml
import sqlite3 as lite
import sys
import json
import os.path
from account_manager import *

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
lentry = False
f_name = False
l_name = False
ddesc = False

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    #get info from txt
    msg = request.values.get('Body', None)
    msg = msg.lower().split()
    user_number = request.values.get('From', None)
    user_number = user_number.replace("+","")
    filename = str("./client/" + user_number)
    #parse msg
    parsed = ""
    for word in msg: 
        parsed += word
    
    global plang
    global ploc
    global pservice
    global lentry
    global f_name
    global l_name
    global ddesc
    #print(checkCity(parsed))
    #if(checkCity(parsed) == "true"):
    #    ploc = parsed
    #    return service()

    if lentry == True:
        f = open(filename,'a')
        f.write("city\n")
        f.write(parsed+"\n")
        f.write("state\n")
        f.write("california\n")
        f.close()    
        lentry = False
        ddesc = True
        return desc()
    elif f_name == True:
        f = open(filename,'a')
        f.write("fName\n")
        f.write(parsed+"\n")
        f.close()    
        f_name = False
        l_name = True
        return lname()
    elif l_name == True:
        f = open(filename,'a')
        f.write("lName\n")
        f.write(parsed+"\n")
        f.close()    
        l_name = False
        return language()
    elif ddesc == True:
        f = open(filename,'a')
        f.write("description\n")
        f.write(parsed+"\n")
        f.close()    
        ddesc = False
        return service()
    
    elif parsed.isdigit() == False:
        if parsed == "service":
            #check if user is subscribed or not
            #add contact if not in client list
            if addContact(user_number) == False:
                f = open(filename,'a')
                f.write("phone\n")
                f.write(user_number+"\n")
                f.write("volunteerID\n")
                f.write("null\n")
                f.close()
                f_name = True
                return fname()    
            return menu()
        elif parsed == "english" or parsed == "spanish":
            f = open(filename,'a')
            f.write("language\n")
            f.write(parsed+"\n")
            f.close()
            return menu()
        elif parsed == "menu":
             return menu()    
        elif parsed == "findvolunteer":
           #language
           lentry = True
           return location()
        elif parsed == "getinfo":
            return about()
        else:
            return
    elif parsed.isdigit() == True:
        for digit in parsed:
            #print digit
            if digit == "1":
               pservice.append("shelter")
            elif digit == "2":
                pservice.append("food")
            elif digit == "3":
                pservice.append("law")

        f = open(filename,'a')
        f.write("tagArray\n")
        for e in pservice:
            f.write(e+"\n")
        f.write("status\n")
        f.write("0\n")
        f.write("EXIT")
        f.close()    
        insertClient(filename)

        match = clientVolunteerMatch(user_number)
        for i in match:
        	print i
        message = client.messages.create(
	    	body= "You will be supporting: " + match[1] + "\n"
	    	"Phone: " + match[2] + "\n" +
	    	"City: " + match[3] + "\n" +
	    	"State: " + match[4] + "\n" +
	    	"Description: " + match[5] + "\n",
	    	to= match[0],
			from_= "16507298318",
		)

        return finished()
    else:
    
        resp = twilio.twiml.Response()
        resp.message("Invalid choice")
        return str(resp)



        #call to create user
        
        #print "preferred lang: " + plang
        #print "location: " + ploc
        #print "services : "
        #for x in pservice:
        #    print x
       
@app.route("/about", methods=['GET', 'POST'])
def about():
    lang = "Get help from a volunteer by completing a questionnaire. Text menu to return to the menu"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp) 

@app.route("/desc", methods=['GET', 'POST'])
def desc():
    lang = "Provide a short description about yourself!"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp) 


@app.route("/fname", methods=['GET', 'POST'])
def fname():
    lang = "What is your first name?"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp) 

@app.route("/lname", methods=['GET', 'POST'])
def lname():
    lang = "What is your last name?"
    resp = twilio.twiml.Response()
    resp.message(lang)
    return str(resp)    


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
    f.write("fName\n")
    f.write( fname+ "\n")
    f.write("lName\n")
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
    f.write("status\n")
    f.write("0\n")
    choice_list = request.form.getlist("choices")
    f.write("tagArray\n")
    for x in choice_list:
        f.write(x + "\n")
    f.write("EXIT")    
    f.close()
    insertVolunteer(filename)
    #os.remove(filename)
    return index()

if __name__ == "__main__":
    app.run(debug=True)