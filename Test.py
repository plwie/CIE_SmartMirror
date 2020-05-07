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
    'clear-day': r"D:\Coding\Project\Smart Mirror\Image/Sun.png",  
    'wind': r"D:\Coding\Project\Smart Mirror\Image/Wind.png",  
    'cloudy': r"D:\Coding\Project\Smart Mirror\Image/Cloud.png",  
    'partly-cloudy-day': r"D:\Coding\Project\Smart Mirror\Image/PartlySunny.png",  
    'rain': r"D:\Coding\Project\Smart Mirror\Image/Rain.png", 
    'fog': r"D:\Coding\Project\Smart Mirror\Image/Haze.png",  
    'clear-night': r"D:\Coding\Project\Smart Mirror\Image/Moon.png",  
    'partly-cloudy-night': r"D:\Coding\Project\Smart Mirror\Image/PartlyMoon.png", 
    'thunderstorm': r"D:\Coding\Project\Smart Mirror\Image/Storm.png",     
    'hail': r"D:\Coding\Project\Smart Mirror\Image/Hail.png"  
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

        self.vbox2 = QVBoxLayout()
        self.clock = Clock()
        self.weather = Weather()
        self.clock.setFixedHeight(150)
        self.covid = Covid(QWidget())
        self.news = News(QWidget)
        self.news.setFixedHeight(300)
        self.covid.setFixedWidth(500)
        self.vbox2.addWidget(self.clock)
        self.vbox2.addStretch()
        self.vbox2.addWidget(self.weather)
        self.vbox2.addStretch()
        self.vbox2.addWidget(self.covid)
        self.vbox2.addStretch()
        self.vbox2.addWidget(self.news)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.vbox2)
        self.setLayout(self.vbox)

        self.show()

class Clock(QWidget):
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 50)
        font2 = QFont('Yikes', 30)

        self.vbox = QVBoxLayout()
        self.time1 = ''
        self.timeLbl = QLabel('')
        self.timeLbl.setAlignment(Qt.AlignLeft)
        self.timeLbl.setFont(font1)
        self.day_of_week1 = ''
        self.dayOWLbl = QLabel('')
        self.dayOWLbl.setFont(QFont('Bavaria',11))
        self.dayOWLbl.setAlignment(Qt.AlignLeft)
        self.date1 = ''
        self.dateLbl = QLabel('')
        self.dateLbl.setFont(QFont('Bavaria',11))
        self.dateLbl.setAlignment(Qt.AlignLeft)
        self.vbox.addWidget(self.timeLbl)
        self.vbox.addWidget(self.dayOWLbl)
        self.vbox.addWidget(self.dateLbl)
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
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
        self.calendar.setStyleSheet("""$background_color : #fcee6d;
$element_highlight : $background_color;
$calendar_color: #29323f;

$day_pill_size : 25px;
$pill_margin : 8px;
html {
  position: relative;
  position: absolute; width:100%; height: 100%;
  left:0; top:0; right:0; bottom: 0;
}

body {
  background-color:desaturate($background_color, 30);
}

section.calendar {
  background-color: $calendar_color;
  font-family: 'Dosis', sans-serif;
  color: #fff;
  width: 290px; padding:45px;
  position: absolute;
  top:50%; left:50%; transform: translateY(-50%) translateX(-50%);
  box-shadow: 5px 10px 20px rgba(0,0,0,.6);
  border-radius:5px;

  h1 {
    text-align: center;
    color: $element_highlight;
    margin: 0 0 30px 0;
  }
  
  form {
    position:relative;
    display: flex;    
    flex-direction: row;
    flex-wrap: wrap;
    align-items: flex-start;
    align-content: flex-start;

    label.weekday{
      display: inline-block;
      width:$day_pill_size; margin: $pill_margin;
      text-align: center;
      color: #999;
    }
    
    form {
      margin:0; padding:0;
      
    }
    
    label.day{
      display: inline-block;
      width:$day_pill_size; margin: $pill_margin;
      
      span {
        display: inline-block;
        width:$day_pill_size; height:$day_pill_size; line-height: $day_pill_size;
        margin: -2px 0 0 -2px;
        border-radius: 50%;
        border: 2px solid $calendar_color;
        text-align:center;
        transition: all .2s linear;
        cursor: pointer;
        
        &:hover {
          
          border-color: darken(desaturate($element_highlight, 20), 10);
        }
      }
      
      em {
        display: inline-block;
        position: absolute;
        border-radius: 50%;
        border-color: $calendar_color;
        width: 3px; height:3px; background-color: darken($element_highlight, 50);
        margin-left:11px; margin-top: 2px;
        opacity: 0;
        transition: all .2s linear;
      }
      
      input[type=text]{
        border:0; opacity:0;
        position:absolute;
        margin-top: 40px; 
        left: -45px; width: 380px; height: 1px; padding: 0;
        outline: none; font-size: 16px;
        transition: height .2s linear, opacity .2s linear, color .02s linear;
        color: #fff;
        
        &:focus{
          opacity: 1;
          height: 35px; padding:10px 40px;
          left: -45px; width: 300px;
          color: $calendar_color;
          
          &+ span {
            color: $element_highlight;
            border-color: $element_highlight;
            background: $element_highlight;
            color: $calendar_color;
            font-weight: bold;
            margin-bottom: 65px;
          }
          
          &~ em {
            border-radius: 0;
            border: 5px solid transparent;
            background: transparent;
            border-bottom-color:rgba(255,255,255,1);
            margin-top:-62px; margin-left:7px;
            width:0; height:0;
            display:inline-block; opacity: 1;
          }
        }
        
        &:valid {
          &+ span {

          }
          &~ em {
            display: inline-block;
            opacity: 1;
          }
        }
        
      }
      
      &.invalid {
        opacity: 0;  width:$day_pill_size; height:$day_pill_size;
        
        span, input {
          display: none;
        }
      }
    }
  }

  
  div.clearfix {
    clear:both;
  }
  
  div.hidden {
    display:none;
  }
  
}""")
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
        font1 = QFont('Times', 17)
        font2 = QFont('Bavaria', 12)
        
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
        font1 = QFont('Times', 18)
        font2 = QFont('Bavaria', 10)
        font3 = QFont('Bavaria', 12)
        #Vbox
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox.addLayout(self.vbox1)
        self.vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        #Heading
        image = cv2.imread(r"D:\Coding\Project\Smart Mirror\Image\Newspaper.png", cv2.IMREAD_COLOR)
        image = cv2.resize(image,(70,70), interpolation = cv2.INTER_AREA)
        image = QImage(image, image.shape[1], image.shape[0], 
                       image.strides[0], QImage.Format_RGB888)
        newspaperIcon = QLabel()
        newspaperIcon.setPixmap(QPixmap.fromImage(image))
        self.vbox1.addWidget(newspaperIcon)
        self.headline = QLabel('Headline')
        self.headline.setFont(font1)
        self.vbox1.addWidget(self.headline)

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
        self.vbox1.addWidget(self.article1)
        self.vbox1.addWidget(self.article2)
        self.vbox1.addWidget(self.article3)

class Covid(QWidget):
    def __init__(self,*args,**kwargs):
        super(Covid,self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Times', 18)
        font2 = QFont('Bavaria', 10)
        font3 = QFont('Bavaria', 12)
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
        infect = str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['confirmed'])
        death = str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['deaths'])
        recover = str(result_covid['Thailand'][len(result_covid['Thailand'])-1]['recovered'])
        #Infected
        self.infectlbl = QLabel('Infected')
        self.infectlbl.setFont(font3)
        self.infect = QLabel(infect)
        self.infect.setFont(font2)
        #Death
        self.deathlbl = QLabel('Death')
        self.deathlbl.setFont(font3)
        self.death = QLabel(death)
        self.death.setFont(font2)
        #Recovered
        self.recoverlbl = QLabel('Recovered')
        self.recover = QLabel(recover)
        self.recoverlbl.setFont(font3)
        self.recover.setFont(font2)

        self.vbox1.addWidget(self.infectlbl)
        self.vbox1.addWidget(self.infect)
        self.vbox1.addWidget(self.deathlbl)
        self.vbox1.addWidget(self.death)
        self.vbox1.addWidget(self.recoverlbl)
        self.vbox1.addWidget(self.recover)
        self.vbox.setContentsMargins(0,0,0,0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
