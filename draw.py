import math
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QTransform, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QToolBar, QPushButton

def dist (p1,p2):
	return math.sqrt ((p1.x()-p2.x())**2 + (p1.y()-p2.y())**2)


class Triangle:
	def __init__(self, b, c, cosA):
		super ().__init__()
		self.b = b
		self.c = c
		self.cosA = cosA
		self.a = a = math.sqrt(b*b+c*c-2*b*c*cosA)
		self.sinA = sinA = math.sqrt (1-cosA*cosA)
		self.cosB = cosB = (a*a+c*c-b*b)/(2*a*c)
		self.sinB = sinB = math.sqrt (1-cosB*cosB)
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

		self.A = QPointF (x1, y1)
		self.B = QPointF (x2, y2)
		self.C = QPointF (x3, y3)

		# Описанная окружность
		D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
		self.x_circ = x_circ = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
		self.y_circ = y_circ = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
		self.R_circ = math.sqrt((x_circ-x1)**2+(y_circ-y1)**2)

		# Вписанная окружность
		self.x_in = (a * x1 + b * x2 + c * x3) / (a + b + c)
		self.y_in = (a * y1 + b * y2 + c * y3) / (a + b + c)
		self.R_in = S / p
		
		# Медианы
		self.A1=QPointF ((x2+x3)/2,(y2+y3)/2)
		self.B1=QPointF ((x1+x3)/2,(y1+y3)/2)
		self.C1=QPointF ((x1+x2)/2,(y1+y2)/2)

		# Высоты
		self.A2=QPointF (x2-c*cosB*cosB,c*cosB*sinB)
		self.B2=QPointF (c*cosA*cosA,c*cosA*sinA)
		self.C2=QPointF (x3,0)
		
		# Биссектрисы
		self.A3=QPointF ((x2*b+x3*c)/(b+c),(y2*b+y3*c)/(b+c))
		self.B3=QPointF ((x1*a+x3*c)/(a+c),(y1*a+y3*c)/(a+c))
		self.C3=QPointF ((x1*a+x2*b)/(a+b),(y1*a+y2*b)/(a+b))

class Draw (QWidget):
	def __init__(self, t: Triangle):
		super ().__init__()
		self.t = t
		self.scaleFactor = 400 / t.c
		self.origScaleFactor = self.scaleFactor
		self.showMedians=False
		self.showAltitudes=False
		self.showBisectors=False
		self.mousePressed=False
		self.mouseStartPosition=None
		self.offsetX = 80
		self.offsetY = 140

	def paintEvent (self, event):
		t = self.t
		A, B, C = t.A, t.B, t.C
		painter=QPainter (self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		transform = QTransform(self.scaleFactor, 0, 0, self.scaleFactor, self.offsetX, self.offsetY)
		painter.setWorldTransform(transform)

		pen = QPen()
		pen.setWidth(2)
		pen.setCosmetic(True)
		painter.setPen(pen)
		
		painter.drawConvexPolygon ([A,B,C])
		
		# Медианы
		if self.showMedians:
			pen.setColor(QColor(255, 0, 0))
			painter.setPen(pen)
			painter.drawLine (A,t.A1)
			painter.drawLine (B,t.B1)
			painter.drawLine (C,t.C1)
			
		# Высоты
		if self.showAltitudes:
			pen.setColor(QColor(Qt.GlobalColor.darkYellow))
			painter.setPen(pen)
			painter.drawLine (A,t.A2)
			painter.drawLine (B,t.B2)
			painter.drawLine (C,t.C2)
			pen.setColor(QColor(Qt.GlobalColor.black))
			pen.setStyle(Qt.PenStyle.DashLine)
			painter.setPen(pen)
			if t.cosA < 0:
				painter.drawLine (A,t.B2)
				painter.drawLine (A,t.C2)
			if t.cosB < 0:
				painter.drawLine (B,t.A2)
				painter.drawLine (B,t.C2)
			if t.cosC < 0:
				painter.drawLine (C,t.A2)
				painter.drawLine (C,t.B2)
			pen.setStyle(Qt.PenStyle.SolidLine)
			
		# Биссектрисы
		if self.showBisectors:
			pen.setColor(QColor(Qt.GlobalColor.magenta))
			painter.setPen(pen)
			painter.drawLine (A,t.A3)
			painter.drawLine (B,t.B3)
			painter.drawLine (C,t.C3)
			
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
		transform = QTransform.fromTranslate(self.offsetX, self.offsetY)
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
		factor=1.001 ** event.angleDelta().y()
		if self.scaleFactor*factor/self.origScaleFactor>10:
			return
		self.scaleFactor *= factor
		x0=event.position().x()-self.offsetX
		y0=event.position().y()-self.offsetY
		self.offsetX=event.position().x()-x0*factor
		self.offsetY=event.position().y()-y0*factor
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
		
	def mousePressEvent (self, event):
		self.mousePressed=True
		self.mouseStartPosition=event.position()
		
	def mouseReleaseEvent (self, event):
		self.mousePressed=False
		
	def mouseMoveEvent (self, event):
		self.offsetX+=event.position().x()-self.mouseStartPosition.x()
		self.offsetY+=event.position().y()-self.mouseStartPosition.y()
		self.mouseStartPosition=event.position()
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

		text='<h3 style="margin-bottom: 0">Стороны</h3>'
		text+=f'AB = {t.c:.1f}<br>'
		text+=f'AC = {t.b:.1f}<br>'
		text+=f'BC = {t.a:.1f}'
		text+='<h3 style="margin-bottom: 0">Углы</h3>'
		text+=f'∠A = {math.acos(t.cosA)/math.pi*180:.0f}°<br>'
		text+=f'∠B = {math.acos(t.cosB)/math.pi*180:.0f}°<br>'
		text+=f'∠C = {math.acos(t.cosC)/math.pi*180:.0f}°'
		text+='<h3 style="margin-bottom: 0">Площадь и периметр</h3>'
		text+=f'S = {t.S:.3f}<br>'
		text+=f'P = {t.a+t.b+t.c:.1f}'
		text+='<h3 style="margin-bottom: 0">Медианы</h3>'
		text+=f'AA<sub>1</sub> = {dist(t.A,t.A1):.3f}<br>'
		text+=f'BB<sub>1</sub> = {dist(t.B,t.B1):.3f}<br>'
		text+=f'CC<sub>1</sub> = {dist(t.C,t.C1):.3f}'
		text+='<h3 style="margin-bottom: 0">Высоты</h3>'
		text+=f'AA<sub>2</sub> = {dist(t.A,t.A2):.3f}<br>'
		text+=f'BB<sub>2</sub> = {dist(t.B,t.B2):.3f}<br>'
		text+=f'CC<sub>2</sub> = {dist(t.C,t.C2):.3f}'
		text+='<h3 style="margin-bottom: 0">Биссектрисы</h3>'
		text+=f'AA<sub>3</sub> = {dist(t.A,t.A3):.3f}<br>'
		text+=f'BB<sub>3</sub> = {dist(t.B,t.B3):.3f}<br>'
		text+=f'CC<sub>3</sub> = {dist(t.C,t.C3):.3f}'
		label=QLabel(text,self)
		font = QFont("Sans", 10)
		label.setFont(font)
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
