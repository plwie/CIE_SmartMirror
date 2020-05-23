import sys
import calendar
import requests
import urllib.request
import time
import json
import pytz
import cv2
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


#For clock
date_format = "%b %d, %Y"
time_format = 12

#For Weather
weather_url = 'https://api.darksky.net/forecast/75bcc50aef1d5aec09148f2849c50db5/13.8816,100.6445/?units=si'
response_weather = requests.get(weather_url)
result_weather = response_weather.json()
icon_lookup = {
    'clear-day': r"/home/pi/Desktop/Smart mirror project/Image/Sun.png",  
    'wind': r"/home/pi/Desktop/Smart mirror project/Image/Wind.png",  
    'cloudy': r"/home/pi/Desktop/Smart mirror project/Image/Cloud.png",  
    'partly-cloudy-day': r"/home/pi/Desktop/Smart mirror project/Image/PartlySunny.png",  
    'rain': r"/home/pi/Desktop/Smart mirror project/Image/Rain.png", 
    'fog': r"/home/pi/Desktop/Smart mirror project/Image/Haze.png",  
    'clear-night': r"/home/pi/Desktop/Smart mirror project/Image/Moon.png",  
    'partly-cloudy-night': r"/home/pi/Desktop/Smart mirror project/Image/PartlyMoon.png", 
    'thunderstorm': r"/home/pi/Desktop/Smart mirror project/Image/Storm.png",     
    'hail': r"/home/pi/Desktop/Smart mirror project/Image/Hail.png"  
}

#For News
news_country_code = 'us'
news_url = 'http://newsapi.org/v2/top-headlines?country=us&apiKey=f7d4f9f59e054ce7932af8ca661626e3'
response_news = requests.get(news_url)
result_news = response_news.json()

#For Covid
covid_url = "https://pomber.github.io/covid19/timeseries.json"
response_covid = requests.get(covid_url)
result_covid = response_covid.json()

class Window(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.title = 'Smart Mirror'
        self.showFullScreen()
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.pal = QPalette()
        self.pal.setColor(QPalette.Background,Qt.black)
        self.pal.setColor(QPalette.Foreground,Qt.white)
        self.setPalette(self.pal)

        self.hbox1 = QHBoxLayout()
        self.clock = Clock(QWidget())
        self.weather = Weather(QWidget())
        self.clock.setFixedHeight(150)
        self.weather.setFixedHeight(150)

        
        self.hbox1.addWidget(self.weather)
        self.hbox1.addStretch()
        self.hbox1.addWidget(self.clock)

        # for Covid
        self.hbox2 = QHBoxLayout()
        self.covid = Covid()
        self.hbox2.addWidget(self.covid)

        #News

        self.hbox3 = QHBoxLayout()
        self.news= News()
        self.hbox3.addWidget(self.news)



        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addStretch()
        self.vbox.addLayout(self.hbox3)
        self.vbox.addStretch()
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)

        self.show()

class Clock(QWidget):
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 30)
        font2 = QFont('Yikes', 10)

        self.vbox = QVBoxLayout()
        self.time1 = ''
        self.timeLbl = QLabel('')
        self.timeLbl.setAlignment(Qt.AlignRight)
        self.timeLbl.setFont(font1)
        self.day_of_week1 = ''
        self.dayOWLbl = QLabel('')
        self.dayOWLbl.setFont(QFont('Bavaria',10))
        self.dayOWLbl.setAlignment(Qt.AlignRight)
        self.date1 = ''
        self.dateLbl = QLabel('')
        self.dateLbl.setFont(QFont('Bavaria',10))
        self.dateLbl.setAlignment(Qt.AlignRight)
        self.vbox.addWidget(self.timeLbl)
        self.vbox.addWidget(self.dayOWLbl)
        self.vbox.addWidget(self.dateLbl)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.setGeometry(50,50,10,10)
        self.time_update()

    def time_update(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def tick(self):

            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.setText(time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.setText(day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.setText(date2)

class Calendar(QWidget):
    global currentYear, currentMonth
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    def __init__(self):
        super().__init__()
        self.calendar = QCalendarWidget(self)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setWindowTitle('Calendar')
        self.resize(350,220)
        self.calendar.setStyleSheet("""border: 1px solid #32414B;
        border-radius: 4px;""")
        self.initUI()

    def initUI(self):
        self.calendar.move(1130, 20)
        self.calendar.setGridVisible(True)
    
        self.calendar.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
        self.calendar.setMaximumDate(QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
    
class Weather(QWidget):
    def __init__(self, *args, **kwargs):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 14)
        font2 = QFont('Bavaria', 10)
        
        #Vbox
        self.vbox= QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox3 = QVBoxLayout()
        #Icon
        self.icon = ''
        self.iconLbl = QLabel()
        self.vbox1.addWidget(self.iconLbl)
        self.vbox1.addStretch()
        icon_id = result_weather['currently']['icon']
        icon2 = None
        if icon_id in icon_lookup:
            icon2 = icon_lookup[icon_id]
        if icon2 is not None:
            if self.icon != icon2:
                self.icon = icon2
                image = cv2.imread(icon2, cv2.IMREAD_COLOR)
                image = cv2.resize(image,(50,50), interpolation = cv2.INTER_CUBIC)
                image = QImage(image, image.shape[1], image.shape[0], 
                    image.strides[0], QImage.Format_RGB888)

                self.iconLbl.setPixmap(QPixmap.fromImage(image))
        else:
            self.iconLbl.setPixmap(QPixmap(''))
            a=1
        #Location
        self.location = QLabel('Bangkok')
        self.location.setFont(font2)
        self.vbox1.addWidget(self.location)
        #Temperature
        degree_sign= u'\N{DEGREE SIGN}'
        temperature = str(int(result_weather['currently']['temperature']))
        temperature2 = "%s%s" % (temperature, degree_sign)
        self.temperature = QLabel(temperature2)
        self.temperature.setFont(font1)
        self.vbox2.addWidget(self.temperature)
        #Current
        current = str(result_weather['currently']['summary'])
        self.current = QLabel(current)
        self.current.setFont(font1)
        self.vbox3.addWidget(self.current)
        self.vbox2.addStretch(1)

        self.vbox.addLayout(self.vbox1)
        self.vbox.addLayout(self.vbox2)
        self.vbox.addLayout(self.vbox3)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)

    def time_convert(timezone,unix_time):
        # get time in tz
        tz = pytz.timezone(timezone)
        dt = datetime.fromtimestamp(unix_time, tz)
        # print it
        return(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

class News(QWidget):
    def __init__(self, source=None):
        super(News, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 12)
        font2 = QFont('Bavaria', 10)
        font3 = QFont('Bavaria', 7)
        #Vbox
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox.addLayout(self.vbox1)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        #Heading
        image = cv2.imread(r"/home/pi/Desktop/Smart mirror project/Image/Newspaper.png", cv2.IMREAD_COLOR)
        image = cv2.resize(image,(50,50), interpolation = cv2.INTER_AREA)
        image = QImage(image, image.shape[1], image.shape[0], 
                       image.strides[0], QImage.Format_RGB888)
        newspaperIcon = QLabel()
        newspaperIcon.setPixmap(QPixmap.fromImage(image))
        self.headline = QLabel('Headline')
        self.headline.setFont(font1)

        #Body
        article1 = str(result_news['articles'][0]['title'])
        article2 = str(result_news['articles'][1]['title'])
        article3 = str(result_news['articles'][2]['title'])
        self.article1 = QLabel(article1)
        self.article2 = QLabel(article2)
        self.article3 = QLabel(article3)
        self.article1.setFont(font3)
        self.article2.setFont(font3)
        self.article3.setFont(font3)
        
        
        self.vbox1.addWidget(newspaperIcon)
        self.vbox1.addWidget(self.headline)
        self.vbox1.addWidget(self.article1)
        self.vbox1.addWidget(self.article2)
        self.vbox1.addWidget(self.article3)


class Covid(QWidget):
    def __init__(self,*args,**kwargs):
        super(Covid,self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 14)
        font2 = QFont('Bavaria', 7)
        font3 = QFont('Bavaria', 10)
        #Vbox
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox.addLayout(self.vbox1)
        self.setLayout(self.vbox)

        #Heading
        self.headline = QLabel('Covid-19 Tracker')
        self.headline.setFont(font1)
        self.vbox1.addWidget(self.headline)

        #Covid data
        infect = ("Infected : " + str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['confirmed']))
        death = ("Death : " + str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['deaths']))
        recover = ("Recovered : " + str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['recovered']))
        #Infected
        self.infect = QLabel(infect)
        self.infect.setFont(font3)
        #Death
        self.death = QLabel(death)
        self.death.setFont(font3)
        #Recovered
        self.recover = QLabel(recover)
        self.recover.setFont(font3)

        self.vbox1.addWidget(self.infect)
        self.vbox1.addWidget(self.death)
        self.vbox1.addWidget(self.recover)
        self.vbox.setContentsMargins(0,0,0,0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
