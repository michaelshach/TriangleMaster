import math
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtWidgets import QApplication, QWidget

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
		painter.drawText (int (b*self.cosA+5), int (b*sinA+10),"C")


if __name__ == '__main__':
	app = QApplication([])
	draw = Draw(1, 1, 0.5)
	draw.show()
	app.exec()
