import math
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel

class Draw (QWidget):
	def __init__(self, b, c, cosA):
		super ().__init__()
		#self.a=a
		self.b=b
		self.c=c
		self.cosA=cosA
		
		self.setWindowTitle ('Окно вывода — TriangleMaster')
	
	def paintEvent (self, event):
		painter=QPainter (self)
		painter.translate(20, 20)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		scaleFactor = 400/self.c
		c = 400
		b = self.b * scaleFactor

		A=QPointF (0, 0)
		B=QPointF (c, 0)
		sinA=math.sqrt (1-self.cosA*self.cosA)
		C=QPointF (b*self.cosA, b*sinA)

		painter.drawConvexPolygon ([A,B,C])
		painter.drawText (-5,-5,"A")
		painter.drawText (c,-5,"B")
		painter.drawText (int (b*self.cosA+5), int (b*sinA+12),"C")

class Window (QWidget):
	def __init__(self, b, c, cosA):
		super ().__init__()
		layout=QHBoxLayout (self)
		draw=Draw (b,c,cosA)
		layout.addWidget(draw, 2)
		
		a=math.sqrt(b*b+c*c-2*b*c*cosA)
		cosB=(a*a+c*c-b*b)/(2*a*c)
		cosC=(a*a+b*b-c*c)/(2*a*b)
		text='<h1>О треугольнике</h1>'
		text+='<h2>Стороны</h2>'
		text+=f'AB = {c:.1f}<br>'
		text+=f'AC = {b:.1f}<br>'
		text+=f'BC = {a:.1f}'
		text+='<h2>Углы</h2>'
		text+=f'∠A = {math.acos(cosA)/math.pi*180:.0f}°<br>'
		text+=f'∠B = {math.acos(cosB)/math.pi*180:.0f}°<br>'
		text+=f'∠C = {math.acos(cosC)/math.pi*180:.0f}°<br>'
		label=QLabel(text,self)
		layout.addWidget(label, 1, Qt.AlignmentFlag.AlignTop)
		

if __name__ == '__main__':
	app = QApplication([])
	window = Window(1, 1, 0.5)
	window.resize(800, 400)
	window.show()
	app.exec()
