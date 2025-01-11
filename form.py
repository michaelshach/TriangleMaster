from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QRadioButton, QWidget, QDoubleSpinBox, QApplication, QButtonGroup, QSizePolicy
import sys
import math
from draw import Window

class Form (QWidget):
	def __init__(self):
		super ().__init__()
		layout = QGridLayout(self)
		label1=QLabel ('Выберите вариант', self)
		layout.addWidget(label1, 0, 0)
		group=QButtonGroup (self)
		self.option1=QRadioButton ('3 стороны')
		self.option1.setChecked  (True)
		group.addButton (self.option1)
		layout.addWidget(self.option1, 1, 0)
		self.option2=QRadioButton ('2 стороны и угол')
		group.addButton (self.option2)
		layout.addWidget(self.option2, 2, 0)
		self.option3=QRadioButton ('сторона и 2 угла')
		group.addButton (self.option3)
		layout.addWidget(self.option3, 3, 0)
		label2=QLabel ('Ввод данных', self)
		layout.addWidget(label2, 0, 1)

		self.spinbox1=QDoubleSpinBox (self)
		self.spinbox1.setRange(1,179.99)
		self.spinbox2=QDoubleSpinBox (self)
		self.spinbox2.setRange(1,179.99)
		self.spinbox3=QDoubleSpinBox (self)
		self.spinbox3.setRange(1,179.99)

		layout.addWidget(self.spinbox1, 1, 1)
		layout.addWidget(self.spinbox2, 2, 1)
		layout.addWidget(self.spinbox3, 3, 1)
		label1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		label2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		button=QPushButton ('Продолжить')
		button.clicked.connect (self.onButtonClicked)
		layout.addWidget (button, 4, 1)
		self.setWindowFlag (Qt.WindowType.WindowMaximizeButtonHint, False)
		self.setWindowTitle ('TriangleMaster')
		self.resize (400, 250)
		
	def onButtonClicked(self):
		if self.option1.isChecked():
			a=self.spinbox1.value()
			b=self.spinbox2.value()
			c=self.spinbox3.value()
			cosA=(b*b+c*c-a*a)/(2*b*c)			
		elif self.option2.isChecked():
			b=self.spinbox1.value()
			c=self.spinbox2.value()
			cosA=math.cos(self.spinbox3.value()/180*math.pi)
		elif self.option3.isChecked():
			c=self.spinbox1.value()
			cosA=math.cos(self.spinbox2.value()/180*math.pi)
			cosB=math.cos(self.spinbox3.value()/180*math.pi)
			sinB=math.sqrt(1-cosB*cosB)
			
			degC=180-self.spinbox2.value()-self.spinbox3.value()
			sinC=math.sin (degC/180*math.pi)
			b=c/sinC*sinB
		self.window=Window(b,c,cosA)
		self.window.resize(800, 400)
		self.window.show ()
		self.window.activateWindow()


def main ():
	app=QApplication (sys.argv)
	form=Form ()
	form.show ()
	app.exec ()


main()
