import math
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtWidgets import QApplication, QWidget

class Draw (QWidget):
	def __init__(self, a, b, c, cosA, cosB):
		super ().__init__()
		self.a=a
		self.b=b
		self.c=c
		self.cosA=cosA
		self.cosB=cosB
	
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
		#painter.drawPoint(A)
		#painter.drawPoint(B)
		#painter.drawPoint(C)
		#painter.end()

if __name__ == '__main__':
	app = QApplication([])
	draw = Draw(1, 1, 1, 0.5, 0.5)
	draw.show()
	app.exec()
