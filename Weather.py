import requests
import urllib.request
import time
import json
import pytz

class Weather(QWidget):
    def __init__(self, *args, **kwargs):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Bavaria', 20)
        font2 = QFont('Bavaria', 10)
        
        #Vbox
        self.vbox= QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        #Temperature
        degree_sign= u'\N{DEGREE SIGN}'
        temperature = str(int(result['currently']['temperature']))
        temperature2 = "%s%s" % (temperature, degree_sign)
        self.temperature = QLabel(temperature2)
        self.temperature.setFont(font1)
        self.hbox.addWidget(self.temperature)
        #Current
        current = str(result['currently']['summary'])
        self.current = QLabel(current)
        self.current.setFont(font1)
        self.vbox2.addWidget(self.current)
        #Forecast
        self.forecastLbl = QLabel('forecast')
        self.forecastLbl.setFont(font1)
        self.vbox2.addWidget(self.forecastLbl)

        self.hbox.setAlignment(Qt.AlignLeft)
        self.vbox2.addStretch(1)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.vbox2)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)

    def time_convert(timezone,unix_time):
        # get time in tz
        tz = pytz.timezone(timezone)
        dt = datetime.fromtimestamp(unix_time, tz)
        # print it
        return(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
