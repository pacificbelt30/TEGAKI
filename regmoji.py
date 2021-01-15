import sys
import json
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import matplotlib.pyplot as plt

class Canvas(QWidget):
    moji_fin = Signal()
    
    def __init__(self):
        super().__init__()
        self.xlist = list()
        self.ylist = list()
        self.image = QImage()
        self.lastpos = QPoint()
        self.is_press = False
        #self.painter = QPainter(self.image)#drawLineのたび呼び出すと効率悪いかもしれないので
        #self.painter.setPen(QPen(Qt.black,2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(300, 300)

    def mousePressEvent(self, event):
        self.is_press = True
        self.lastpos = event.pos()
        self.xlist.append(list())
        self.ylist.append(list())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_press:
            self.is_press = False
            self.drawLine(event.pos())
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_press:
            self.drawLine(event.pos())

    def drawLine(self,endpos):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.black,2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastpos, endpos)
        self.lastpos = QPoint(endpos)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = event.rect()
        painter.drawImage(rect, self.image, rect)

    def resizeEvent(self, event):
        if self.image.width() < self.width() or self.image.height() < self.height():
            changeWidth = max(self.width(), self.image.width())
            changeHeight = max(self.height(), self.image.height())
            self.resizeImage(self.image, QSize(changeWidth, changeHeight))
            self.update()

    def resizeImage(self, image, newSize):
        changeImage = QImage(newSize, QImage.Format_RGB32)
        changeImage.fill(qRgb(255, 255, 255))
        painter = QPainter(changeImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = changeImage



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "test"
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.show()
        self.setWindowLayout()

    def setWindowLayout(self):
        self.canvas = Canvas()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
