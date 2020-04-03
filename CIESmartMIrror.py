import sys
import time
import calendar
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QDate, QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QIcon

date_format = "%b %d, %Y"
time_format = 12


class Window(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.title = 'Smart Mirror'
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 840, 700)
        self.pal = QPalette()
        self.pal.setColor(QPalette.Background,Qt.black)
        self.pal.setColor(QPalette.Foreground,Qt.white)
        self.setPalette(self.pal)

    #HBox1 {Clock,Calendar}
        Hbox1 = QHBoxLayout()
        self.calendar = Calendar()
        self.calendar.setFixedHeight(150)
        self.clock = Clock()
        self.clock.setFixedHeight(150)
        Hbox1.addWidget(self.clock)
        Hbox1.addWidget(self.calendar)
        self.setLayout(Hbox1)
        
        
        self.show()


class Clock(QWidget):
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Bavaria', 50)
        font2 = QFont('Bavaria', 30)

        self.vbox = QVBoxLayout()
        self.time1 = ''
        self.timeLbl = QLabel('')
        self.timeLbl.setAlignment(Qt.AlignRight)
        self.timeLbl.setFont(font1)
        self.day_of_week1 = ''
        self.dayOWLbl = QLabel('')
        self.dayOWLbl.setAlignment(Qt.AlignRight)
        self.date1 = ''
        self.dateLbl = QLabel('')
        self.dateLbl.setAlignment(Qt.AlignRight)
        self.vbox.addWidget(self.timeLbl)
        self.vbox.addWidget(self.dayOWLbl)
        self.vbox.addWidget(self.dateLbl)
        self.vbox.addStretch(2)
        self.vbox.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.time_update()

    def time_update(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def tick(self):

            if time_format == 24:
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
        self.setWindowTitle('Calendar')
        self.resize(350,220)
        self.initUI()

    def initUI(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.NoVerticalHeader
        self.calendar.move(20, 20)
        self.calendar.setGridVisible(True)
        

        self.calendar.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
        self.calendar.setMaximumDate(QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))

    

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
