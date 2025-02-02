import math
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QTransform, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel

class Triangle:
	def __init__(self, b, c, cosA):
		super ().__init__()
		self.b = b
		self.c = c
		self.cosA = cosA
		self.a = a = math.sqrt(b*b+c*c-2*b*c*cosA)
		self.sinA = sinA = math.sqrt (1-cosA*cosA)
		self.cosB = (a*a+c*c-b*b)/(2*a*c)
		self.cosC = (a*a+b*b-c*c)/(2*a*b)
		self.p = p = (a+b+c)/2
		self.S = S = math.sqrt(p*(p-a)*(p-b)*(p-c))

		# Координаты вершин
		self.x1 = x1 = 0
		self.y1 = y1 = 0
		self.x2 = x2 = c
		self.y2 = y2 = 0
		self.x3 = x3 = b * self.cosA
		self.y3 = y3 = b * sinA

		# Описанная окружность
		D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
		self.x_circ = x_circ = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
		self.y_circ = y_circ = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
		self.R_circ = math.sqrt((x_circ-x1)**2+(y_circ-y1)**2)

		# Вписанная окружность
		self.x_in = (a * x1 + b * x2 + c * x3) / (a + b + c)
		self.y_in = (a * y1 + b * y2 + c * y3) / (a + b + c)
		self.R_in = S / p


class Draw (QWidget):
	def __init__(self, t: Triangle):
		super ().__init__()
		self.t = t
	
	def paintEvent (self, event):
		t = self.t
		painter=QPainter (self)
		scaleFactor = 400 / t.c
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		transform = QTransform(scaleFactor, 0, 0, scaleFactor, 80, 140)
		painter.setWorldTransform(transform)

		pen = QPen()
		pen.setWidth(2)
		pen.setCosmetic(True)
		painter.setPen(pen)

		A = QPointF (t.x1, t.y1)
		B = QPointF (t.x2, t.y2)
		C = QPointF (t.x3, t.y3)
		painter.drawConvexPolygon ([A,B,C])

		# Описанная окружность
		pen.setColor(QColor(0, 255, 0))
		painter.setPen(pen)
		center = QPointF(t.x_circ, t.y_circ)
		painter.drawEllipse(center, t.R_circ, t.R_circ)

		# Вписанная окружность
		pen.setColor(QColor(0, 0, 255))
		painter.setPen(pen)
		center = QPointF(t.x_in, t.y_in)
		painter.drawEllipse(center, t.R_in, t.R_in)

		# Буквы для вершин
		pen.setColor(QColor(0, 0, 0))
		painter.setPen(pen)
		font = QFont("Sans", 14)
		painter.setFont(font)
		transform = QTransform.fromTranslate(80, 140)
		painter.setWorldTransform(transform)
		x1 = t.x1 * scaleFactor
		y1 = t.y1 * scaleFactor
		x2 = t.x2 * scaleFactor
		y2 = t.y2 * scaleFactor
		x3 = t.x3 * scaleFactor
		y3 = t.y3 * scaleFactor
		painter.drawText(int(x1)-5, int(y1)-5, "A")
		painter.drawText(int(x2), int(y2)-5, "B")
		painter.drawText(int(x3)+5, int(y3)+12, "C")

class Window (QWidget):
	def __init__(self, b, c, cosA):
		super ().__init__()
		self.setWindowTitle('Окно вывода — TriangleMaster')
		layout=QHBoxLayout (self)
		t = Triangle(b, c, cosA)
		draw=Draw (t)
		layout.addWidget(draw, 2)

		text='<h1>О треугольнике</h1>'
		text+='<h2>Стороны</h2>'
		text+=f'AB = {t.c:.1f}<br>'
		text+=f'AC = {t.b:.1f}<br>'
		text+=f'BC = {t.a:.1f}'
		text+='<h2>Углы</h2>'
		text+=f'∠A = {math.acos(t.cosA)/math.pi*180:.0f}°<br>'
		text+=f'∠B = {math.acos(t.cosB)/math.pi*180:.0f}°<br>'
		text+=f'∠C = {math.acos(t.cosC)/math.pi*180:.0f}°'
		text+='<h2>Площадь и периметр</h2>'
		text+=f'S = {t.S:.3f}<br>'
		text+=f'P = {t.a+t.b+t.c:.1f}'
		label=QLabel(text,self)
		layout.addWidget(label, 1, Qt.AlignmentFlag.AlignTop)
		

if __name__ == '__main__':
	app = QApplication([])
	window = Window(1, 1, 0.5)
	window.resize(1000, 600)
	window.show()
	app.exec()
