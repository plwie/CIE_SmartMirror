import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget
from PyQt5.QtCore import QDate

class Calendar(QWidget):
	global currentYear, currentMonth
	currentMonth = datetime.now().month
	currentYear = datetime.now().year

    

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Calendar')
		self.setGeometry(300, 300, 350, 200)
		self.initUI()

	def initUI(self):
		self.calendar = QCalendarWidget(self)
		self.calendar.move(20, 20)
		self.calendar.setGridVisible(True)

		self.calendar.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
		self.calendar.setMaximumDate(QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))




def window():
	app = QApplication(sys.argv)
	calendar = Calendar()
	calendar.show()
	sys.exit(app.exec_())

window()