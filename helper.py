import os.path

cities = ["sanfrancisco", "sanjose", "santacruz", "losangeles"]
contacts = []

def checkCity(city_name):
    for city in cities:
    	if(city_name == city):
    		return "true"
    return "false"


def addContact(potential):
	potential = str("./client/" + potential)
	print potential
	return os.path.exists(potential)

def removeContact(client):
    for contact in contacts:
        if client == contact:
            contacts.remove(client)
            return True
    return False       

