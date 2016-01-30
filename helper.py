cities = {"sanfrancisco", "sanjose", "santacruz", "losangeles"}

def checkCity(city_name):
    for city in cities:
    	if(city_name == city):
    		return "true"
    return "false"