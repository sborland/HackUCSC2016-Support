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

