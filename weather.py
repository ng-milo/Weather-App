import json
import requests


# '''
class weatherStats:
    location = ''
    country = ''
    timezone = ''
    temps = ''
    conditions = ''
    feels = ''
    quality = ''

    def __init__(self, inputFile):
        self.location = inputFile["location"]["name"]
        self.country = inputFile["location"]["country"]
        self.timezone = inputFile["location"]["tz_id"]
        self.temps = inputFile["current"]["temp_c"]
        self.conditions = inputFile["current"]["condition"]
        self.feels = inputFile["current"]["feelslike_c"]
        self.quality = inputFile["current"]["air_quality"]["gb-defra-index"]

    def setupData(inputFile):
        location = inputFile["location"]["name"]
        country = inputFile["location"]["country"]
        timezone = inputFile["location"]["tz_id"]
        temps = inputFile["current"]["temp_c"]
        conditions = inputFile["current"]["condition"]
        feels = inputFile["current"]["feelslike_c"]
        quality = inputFile["current"]["air_quality"]["gb-defra-index"]
        pass

# '''


def dataUpdater(fileOp, weatherHolder):
    pass


def jsonGetter(key):
    # Recieves key and opens the file
    apiCall = "https://api.weatherapi.com/v1/current.json?key==v7e6h2&aqi=yes"
    index = apiCall.find("=v7e6h2&aqi=yes")
    finapiCall = apiCall[:index] + key + apiCall[index:]
    response = requests.get(apiCall).json()
    with open('result.json', 'w') as fp:
        json.dump(response, fp)
    opFile = open("result.json")
    files = json.load(opFile)
    return files


def prettyPrint(files):
    # Pretty prints the json file for easier debugging
    formattedFile = json.dumps(files, indent=2)
    print(formattedFile)
    pass
