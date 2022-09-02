import sys
from tkinter import HORIZONTAL
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
from weather import *
import json
import requests
import geocoder

"""
This is the weather class
that is used to update the information
and store the data for easy access
"""


class weatherStats:
    location = ''
    temps = ''
    feels = ''
    conditions = ''
    maxTemp = ''
    minTemp = ''

    def __init__(self):
        inputFile = open('result.json')
        data = json.load(inputFile)
        self.location = str(data['location']['name'])
        self.temps = str(data['current']['temp_c'])
        self.feels = str(data['current']['feelslike_c'])
        self.conditions = str(data['current']['condition']['text'])
        self.maxTemp = str(data['forecast']['forecastday']
                           [0]['day']['maxtemp_c'])
        self.minTemp = str(data['forecast']['forecastday']
                           [0]['day']['mintemp_c'])
        inputFile.close()

    def makeUpdates(self):
        inputFile = open('result.json')
        data = json.load(inputFile)
        self.location = str(data['location']['name'])
        self.temps = str(data['current']['temp_c'])
        self.feels = str(data['current']['feelslike_c'])
        self.conditions = str(data['current']['condition']['text'])
        self.maxTemp = str(data['forecast']['forecastday']
                           [0]['day']['maxtemp_c'])
        self.minTemp = str(data['forecast']['forecastday']
                           [0]['day']['mintemp_c'])
        inputFile.close()


def updateFile(userAPI):
    # Need to get api key, and also get the location of user
    ip = geocoder.ip("me")
    spaces = ' '
    APIKey = str(userAPI)
    longLat = str(ip.latlng[0])
    longLat += spaces
    longLat += str(ip.latlng[1])

    # Build the function to call the API
    apiCall = 'https://api.weatherapi.com/v1/forecast.json?key='
    apiCall += APIKey
    apiCall += '&q='
    apiCall += longLat
    apiCall += '&days=7&aqi=yes&alerts=yes'

    # Call the API to get data
    # Place data in json file
    response = requests.get(apiCall)
    jsonResponse = response.json()
    # response.status_code must == 200 for it to be valid
    with open('result.json', 'w') as fp:
        json.dump(jsonResponse, fp)
    opFile = open('result.json')
    files = json.load(opFile)
    pass


"""
    This is the main window class
    It will contain all the widgets
    and the layout of the window
"""


class window(QMainWindow):
    apiKey = ''
    locTemp = ''
    felLike = ''
    hiLow = ''
    weatherInfo = ''
    curWeather = ''

    def __init__(self):
        super().__init__()
        self.weatherInfo = weatherStats()
        self.getAPI()
        self.initUI()
        if (self.apiKey != ''):
            updateFile(self.apiKey)
            self.weatherInfo.makeUpdates()
        """

        This is for the Main Forcast

        """
        # Create a central widget
        layout = QVBoxLayout()
        # Make Text for everything correct
        tempText = self.weatherInfo.location + "\n" + self.weatherInfo.temps + "°C"
        weatherText = self.weatherInfo.conditions
        feelsText = "Feels Like: " + self.weatherInfo.feels + "°C"
        lowhiText = "H: " + self.weatherInfo.maxTemp + "°C     |     L: "
        lowhiText += self.weatherInfo.minTemp + "°C"
        # Create a label for the information
        self.locTemp = QLabel(tempText, self)
        self.curWeather = QLabel(weatherText, self)
        self.felLike = QLabel(feelsText, self)
        self.hiLow = QLabel(lowhiText, self)
        # Set font sizes for the different labels
        font1 = self.locTemp.font()
        font2 = self.felLike.font()
        font3 = self.hiLow.font()
        font4 = self.curWeather.font()
        font1.setPointSize(35)
        font2.setPointSize(15)
        font3.setPointSize(12)
        font4.setPointSize(18)
        self.locTemp.setFont(font1)
        self.felLike.setFont(font2)
        self.hiLow.setFont(font3)
        self.curWeather.setFont(font4)
        # Add the labels to the layout
        layout.addWidget(self.locTemp)
        layout.addWidget(self.curWeather)
        layout.addWidget(self.felLike)
        layout.addWidget(self.hiLow)
        # Center the words
        self.locTemp.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.felLike.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.hiLow.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.curWeather.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        # Ensures that everything is bundled together
        layout.insertStretch(-1, 1)
        self.setCentralWidget(widget)

        """

        This is to update the temperature every hour

        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.mainForcast)
        self.timer.start(1800000)
        self.settings()

    def initUI(self):
        self.setGeometry(900, 350, 640, 680)
        self.setWindowTitle('Weather App')
        self.show()

    def weeklyForcast(self):
        pass

    def hourlyForcast(self):
        pass

    def mainForcast(self):
        if (self.apiKey != ''):
            updateFile(self.apiKey)
            self.weatherInfo.makeUpdates()
        tempText = self.weatherInfo.location + "\n" + self.weatherInfo.temps + "°C"
        weatherText = self.weatherInfo.conditions
        feelsText = "Feels Like: " + self.weatherInfo.feels + "°C"
        lowhiText = "H: " + self.weatherInfo.maxTemp + "°C     |     L: "
        lowhiText += self.weatherInfo.minTemp + "°C"
        self.locTemp.setText(tempText)
        self.curWeather.setText(weatherText)
        self.felLike.setText(feelsText)
        self.hiLow.setText(lowhiText)
        pass

    def settings(self):
        # Create a menu bar
        mainMenu = self.menuBar()
        pyGuiMenu = mainMenu.addMenu('Settings')
        # Create GUI to receive API key
        subItemTable = QAction('API', self)
        subItemTable.setStatusTip("Set API Key")
        subItemTable.triggered.connect(self.getAPI)
        pyGuiMenu.addAction(subItemTable)
        # Create GUI to exit application
        subItemExit = QAction('Exit', self)
        subItemExit.setShortcut("Ctrl+Q")
        subItemExit.setStatusTip("Exit Application")
        subItemExit.triggered.connect(self.closeApp)
        pyGuiMenu.addAction(subItemExit)
        pass

    def background(self):
        pass

    def closeApp(self):
        reply = QMessageBox.question(
            self,
            "Exit Application",
            "Are you certain you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            sys.exit()
        pass

    def getAPI(self):
        temp = QInputDialog.getText(self, 'API Key', 'Enter API Key:')
        self.apiKey = temp[0]
        pass


def main():
    # Initialize the weather stats first

    # Initialize the GUI
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("EncodeSansCondensed-ExtraLight.ttf")
    app.setStyleSheet(
        "QLabel{font-family: Encode Sans Condensed ExLight; color: black;}")
    ex = window()
    # Locks the Window Size
    ex.setFixedSize(640, 680)
    # ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
