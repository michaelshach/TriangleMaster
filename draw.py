import math
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QTransform, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QToolBar, QPushButton

class Triangle:
	def __init__(self, b, c, cosA):
		super ().__init__()
		self.b = b
		self.c = c
		self.cosA = cosA
		self.a = a = math.sqrt(b*b+c*c-2*b*c*cosA)
		self.sinA = sinA = math.sqrt (1-cosA*cosA)
		self.cosB = cosB = (a*a+c*c-b*b)/(2*a*c)
		self.sinB = math.sqrt (1-cosB*cosB)
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
		self.scaleFactor = 400 / t.c
		self.showMedians=False
		self.showAltitudes=False
		self.showBisectors=False

	def paintEvent (self, event):
		t = self.t
		painter=QPainter (self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		transform = QTransform(self.scaleFactor, 0, 0, self.scaleFactor, 80, 140)
		painter.setWorldTransform(transform)

		pen = QPen()
		pen.setWidth(2)
		pen.setCosmetic(True)
		painter.setPen(pen)
		
		A = QPointF (t.x1, t.y1)
		B = QPointF (t.x2, t.y2)
		C = QPointF (t.x3, t.y3)
		painter.drawConvexPolygon ([A,B,C])
		
		# Медианы
		if self.showMedians:
			K=QPointF ((t.x2+t.x3)/2,(t.y2+t.y3)/2)
			L=QPointF ((t.x1+t.x3)/2,(t.y1+t.y3)/2)
			M=QPointF ((t.x1+t.x2)/2,(t.y1+t.y2)/2)
			pen.setColor(QColor(255, 0, 0))
			painter.setPen(pen)
			painter.drawLine (A,K)
			painter.drawLine (B,L)
			painter.drawLine (C,M)
			
		# Высоты
		if self.showAltitudes:
			K=QPointF (t.x2-t.c*t.cosB*t.cosB,t.c*t.cosB*t.sinB)
			L=QPointF (t.c*t.cosA*t.cosA,t.c*t.cosA*t.sinA)
			M=QPointF (t.x3,0)
			pen.setColor(QColor(Qt.GlobalColor.darkYellow))
			painter.setPen(pen)
			painter.drawLine (A,K)
			painter.drawLine (B,L)
			painter.drawLine (C,M)
			pen.setColor(QColor(Qt.GlobalColor.black))
			pen.setStyle(Qt.PenStyle.DashLine)
			painter.setPen(pen)
			if t.cosA < 0:
				painter.drawLine (A,M)
				painter.drawLine (A,L)
			if t.cosB < 0:
				painter.drawLine (B,K)
				painter.drawLine (B,M)
			if t.cosC < 0:
				painter.drawLine (C,K)
				painter.drawLine (C,L)
			pen.setStyle(Qt.PenStyle.SolidLine)
			
		# Биссектрисы
		if self.showBisectors:
			K=QPointF ((t.x2*t.b+t.x3*t.c)/(t.b+t.c),(t.y2*t.b+t.y3*t.c)/(t.b+t.c))
			L=QPointF ((t.x1*t.a+t.x3*t.c)/(t.a+t.c),(t.y1*t.a+t.y3*t.c)/(t.a+t.c))
			M=QPointF ((t.x1*t.a+t.x2*t.b)/(t.a+t.b),(t.y1*t.a+t.y2*t.b)/(t.a+t.b))
			pen.setColor(QColor(Qt.GlobalColor.magenta))
			painter.setPen(pen)
			painter.drawLine (A,K)
			painter.drawLine (B,L)
			painter.drawLine (C,M)
			
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
		x1 = t.x1 * self.scaleFactor
		y1 = t.y1 * self.scaleFactor
		x2 = t.x2 * self.scaleFactor
		y2 = t.y2 * self.scaleFactor
		x3 = t.x3 * self.scaleFactor
		y3 = t.y3 * self.scaleFactor
		painter.drawText(int(x1)-5, int(y1)-5, "A")
		painter.drawText(int(x2), int(y2)-5, "B")
		painter.drawText(int(x3)+5, int(y3)+12, "C")
	
	def wheelEvent(self, event):
		self.scaleFactor *= (1.001 ** event.angleDelta().y())
		self.repaint()

	def toggleMedians (self, checked):
		self.showMedians=checked
		self.repaint ()
		
	def toggleAltitudes (self, checked):
		self.showAltitudes=checked
		self.repaint ()
		
	def toggleBisectors (self, checked):
		self.showBisectors=checked
		self.repaint()
		
class Window (QWidget):
	
	def __init__(self, b, c, cosA):
		super ().__init__()
		self.setWindowTitle('Окно вывода — TriangleMaster')
		vLayout = QVBoxLayout(self)
		hLayout = QHBoxLayout()
		vLayout.addLayout(hLayout)
		t = Triangle(b, c, cosA)
		draw=Draw (t)
		hLayout.addWidget(draw, 2)

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
		hLayout.addWidget(label, 1, Qt.AlignmentFlag.AlignTop)
		mediansButton=QPushButton ('Показать медианы')
		mediansButton.setCheckable (True)
		mediansButton.toggled.connect (draw.toggleMedians)
		altitudesButton=QPushButton ('Показать высоты')
		altitudesButton.setCheckable (True)
		altitudesButton.toggled.connect (draw.toggleAltitudes)
		bisectorsButton=QPushButton ('Показать биссектрисы')
		bisectorsButton.setCheckable (True)
		bisectorsButton.toggled.connect (draw.toggleBisectors)
		hLayout2=QHBoxLayout ()
		hLayout2.addWidget(mediansButton)
		hLayout2.addWidget(altitudesButton)
		hLayout2.addWidget(bisectorsButton)
		vLayout.addLayout (hLayout2)

if __name__ == '__main__':
	app = QApplication([])
	window = Window(1, 1, 0.5)
	window.resize(1000, 600)
	window.show()
	app.exec()
