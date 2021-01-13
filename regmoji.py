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
        self.canvas_width = 600
        self.canvas_height = 600
        self.xlist = list()
        self.ylist = list()
        self.kakusu = 99
        self.count = 0  # 画数カウント
        self.image = QImage()
        self.lastpos = QPoint()
        self.is_press = False
        self.paintable = True
        # self.painter = QPainter(self.image)#drawLineのたび呼び出すと効率悪いかもしれないので
        # self.painter.setPen(QPen(Qt.black,2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setGeometry(self.canvas_width, self.canvas_height, self.canvas_width, self.canvas_height)
        self.setFixedSize(self.canvas_width, self.canvas_height)

    def setKakusu(self, kakusu):
        self.kakusu = kakusu
        if self.kakusu < 1:
            self.kakusu = 99

    def mousePressEvent(self, event):
        self.is_press = True
        self.lastpos = event.pos()
        self.xlist.append(list())
        self.ylist.append(list())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_press:
            self.is_press = False
            self.drawLine(event.pos())
            self.count = self.count + 1

            if self.count == self.kakusu:
                self.moji_fin.emit()
                self.clear()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_press:
            self.drawLine(event.pos())

    def drawLine(self, endpos):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastpos, endpos)
        self.lastpos = QPoint(endpos)
        self.xlist[self.count].append(self.lastpos.x())
        self.ylist[self.count].append(self.lastpos.y())
        # print(self.xlist)
        self.update()

    def clear(self):
        self.xlist = list()
        self.ylist = list()
        self.count = 0
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        rect = QRect(0, 0, self.canvas_width, self.canvas_height)
        painter.fillRect(rect, Qt.white)
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
        self.title = "文字登録"
        self.width = 800
        self.height = 800
        self.text = ["あ", "い", "う", "え", "お"]
        self.kakusu = [3, 2, 2, 2, 3]
        self.count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.show()
        self.setWindowLayout()

    def setWindowLayout(self):
        self.label = QLabel()
        self.label.setText(self.text[self.count]+"を書いてください"+str(self.kakusu[self.count])+"画")
        self.canvas = Canvas()
        self.canvas.setKakusu(self.kakusu[self.count])
        self.canvas.moji_fin.connect(self.save_data)
        self.button = QPushButton()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    @Slot()
    def save_data(self):
        print('count==3')
        plt.xlim(0, self.canvas.canvas_width)
        plt.ylim(self.canvas.canvas_height, 0)
        for i in range(len(self.canvas.xlist)):
            plt.plot(self.canvas.xlist[i], self.canvas.ylist[i])
            print(str(i)+'画目'+str(len(self.canvas.xlist[i]))+' '+str(len(self.canvas.ylist[i])))
        # plt.plot(self.canvas.xlist[0], self.canvas.ylist[0])
        # plt.plot(self.canvas.xlist[1], self.canvas.ylist[1])
        # plt.plot(self.canvas.xlist[2], self.canvas.ylist[2])
        # print('一画目'+str(len(self.canvas.xlist[0]))+' '+str(len(self.canvas.ylist[0])))
        # print('二画目'+str(len(self.canvas.xlist[1]))+' '+str(len(self.canvas.ylist[1])))
        # print('三画目'+str(len(self.canvas.xlist[2]))+' '+str(len(self.canvas.ylist[2])))
        tmp = {self.text[self.count]: {"data": {"x": self.canvas.xlist, "y": self.canvas.ylist}}}
        json.dumps(tmp)
        with open('test.json', 'a') as f:
        #with open('test.json', 'w') as f:
            json.dump(tmp, f, indent=4)
        plt.show()
        self.canvas.clear()
        self.field_update()

    def field_update(self):
        self.count = self.count + 1
        if self.count < len(self.text):
            self.label.setText(self.text[self.count]+"を書いてください"+str(self.kakusu[self.count])+"画")
            self.canvas.setKakusu(self.kakusu[self.count])
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
