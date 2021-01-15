import sys
import json
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsView
from PyQt5.QtGui import QPainter, QImage, QPen, qRgb, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal, pyqtSlot
import matplotlib.pyplot as plt

class Canvas(QWidget):
  moji_fin=pyqtSignal()
  def __init__(self):
    super().__init__()
    self.countx = list()
    self.county = list()
    self.kakusu = 99
    self.text = ""
    self.count = 0
    self.myPenWidth = 2
    self.myPenColor = Qt.black
    self.image = QImage()
    # これを消したら右クリックを押したときにも線が描かれちゃうよ
    self.check = False
    self.initUI()

  def initUI(self):
    self.setGeometry(300, 300, 300, 300)
    self.setFixedSize(300,300)
    #self.setWindowTitle("Canvas")
    #self.show()

  def mousePressEvent(self, event):
    # マウスの左クリックが押されたときに処理が動くよ。賢いね
    if event.button() == Qt.LeftButton:
      # クリックした位置を保存しておくよ
      self.lastPos = event.pos()
      # 無事に左クリックが押されたからTrueにしておくよ
      self.check = True
      self.countx.append(list())
      self.county.append(list())

  def mouseMoveEvent(self, event):
    # buttonsになっているから気をつけようね
    if event.buttons() and Qt.LeftButton and self.check:
      # 線を引くよ
      self.drawLine(event.pos())

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton and self.check:
      self.drawLine(event.pos())
      # 左クリックが離されたらまたクリックしたときのためにFalseにするよ
      self.check = False

      self.count = self.count+1
      if self.count == self.kakusu:
          self.moji_fin.emit()
          #print('count==3')
          #plt.xlim(0,500)
          #plt.ylim(500,0)
          #plt.plot(self.countx[0],self.county[0])
          #plt.plot(self.countx[1],self.county[1])
          #plt.plot(self.countx[2],self.county[2])
          #print('一画目'+str(len(self.countx[0]))+' '+str(len(self.county[0])))
          #print('二画目'+str(len(self.countx[1]))+' '+str(len(self.county[1])))
          #print('三画目'+str(len(self.countx[2]))+' '+str(len(self.county[2])))
          #tmp = {self.text:{"data":{"x":self.countx,"y":self.county}}}
          #json.dumps(tmp)
          #with open('test.json', 'w') as f:
              #json.dump(tmp, f, indent=4)
          #self.clear()
          #plt.show()

  def clear(self):
    self.countx = list()
    self.county = list()
    self.count = 0
    painter = QPainter(self.image)
    painter.setPen(
      QPen(Qt.white)
    )
    rect = QRect(0, 0, 300, 300)
    painter.fillRect(rect, Qt.white)
    self.update()


  def drawLine(self, endPos):
    # 線を引くよ
    painter = QPainter(self.image)
    # ペンの設定だよ左から色、太さ、線の種類、線の端を丸くするか、線の角を丸くするか
    painter.setPen(
      QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    )
    # クリックした位置からマウスを離した位置まで線を引いていくよ
    painter.drawLine(self.lastPos, endPos)
    # アップデートしてあげようね
    self.update()#このとき，paintEventが呼ばれると考えられる．
    self.countx[self.count].append(self.lastPos.x())
    self.county[self.count].append(self.lastPos.y())
    #print(self.countx+self.county+endPos)
    print('countx=')
    print(self.countx)
    print('county=')
    print(self.county)
    print(endPos)
    print(self.count)
    # クリックを離した位置を保存しておくよ
    self.lastPos = QPoint(endPos)

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
        self.title="test"
        self.text = "あ"
        self.kakusu = 3
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
        self.button = QPushButton()
        self.label = QLabel("「"+self.text+"」"+"を描いてください")
        self.canvas.kakusu = self.kakusu
        self.canvas.text = self.text
        self.canvas.moji_fin.connect(self.save_data)
        self.layout = QVBoxLayout()
        #self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    # 描画データを保存し，まっさらにするスロット
    @pyqtSlot()
    def save_data(self):
        print('count==3')
        plt.xlim(0,500)
        plt.ylim(500,0)
        plt.plot(self.canvas.countx[0],self.canvas.county[0])
        plt.plot(self.canvas.countx[1],self.canvas.county[1])
        plt.plot(self.canvas.countx[2],self.canvas.county[2])
        print('一画目'+str(len(self.canvas.countx[0]))+' '+str(len(self.canvas.county[0])))
        print('二画目'+str(len(self.canvas.countx[1]))+' '+str(len(self.canvas.county[1])))
        print('三画目'+str(len(self.canvas.countx[2]))+' '+str(len(self.canvas.county[2])))
        tmp = {self.text:{"data":{"x":self.canvas.countx,"y":self.canvas.county}}}
        json.dumps(tmp)
        with open('test.json', 'a') as f:
        #with open('test.json', 'w') as f:
            json.dump(tmp, f, indent=4)
        self.canvas.clear()
        plt.show()



if __name__ == '__main__':
  # 動け～
  app = QApplication(sys.argv)
  #ex = Canvas()
  ex = MainWindow()
  sys.exit(app.exec_())
