import sys
import json
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import matplotlib.pyplot as plt
from dataquery import *


class Canvas(QWidget):
    moji_fin:Signal = Signal() # 文字を書き終わったときに放出
    oneline_fin:Signal = Signal() # 1画描き終わったときに放出

    def __init__(self):
        super().__init__()
        self._canvas_width:int = 600
        self._canvas_height:int = 600
        self._xlist:list = list()
        self._ylist:list = list()
        self._kakusu:int = 99
        self._count:int = 0  # 画数カウント
        self._image:QImage = QImage()
        self._lastpos:QPoint = QPoint()
        self._is_press:bool = False
        #self._paintable:bool = True
        # self.painter = QPainter(self.image)#drawLineのたび呼び出すと効率悪いかもしれないので
        # self.painter.setPen(QPen(Qt.black,2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setGeometry(self.canvas_width, self.canvas_height, self.canvas_width, self.canvas_height)
        self.setFixedSize(self.canvas_width, self.canvas_height)

    # property, setter define
    @property
    def canvas_width(self) ->int:
        return self._canvas_width
    @property
    def canvas_height(self) ->int:
        return self._canvas_height
    @property
    def xlist(self) -> list:
        return self._xlist
    @xlist.setter
    def xlist(self,x:list):
        self._xlist = x
    @property
    def ylist(self) -> list:
        return self._ylist
    @ylist.setter
    def ylist(self,y:list):
        self._ylist = y
    @property
    def kakusu(self) -> int:
        return self._kakusu
    @kakusu.setter
    def kakusu(self,kakusu:int):
        self._kakusu = kakusu
    @property
    def count(self) -> int:
        return self._count
    @count.setter
    def count(self,count:int):
        self._count = count
    @property
    def image(self) -> QImage:
        return self._image
    @image.setter
    def image(self,image:QImage):
        self._image = image
    @property
    def lastpos(self) -> QPoint:
        return self._lastpos
    @lastpos.setter
    def lastpos(self,lastpos:QPoint):
        self._lastpos = lastpos
    @property
    def is_press(self) -> bool:
        return self._is_press
    @is_press.setter
    def is_press(self,press:bool):
        self._is_press = press

    # 描く文字の画数をセット
    def setKakusu(self, num):
        self.kakusu = num
        if self.kakusu < 1:
            self.kakusu = 99

    # 左クリックを押したとき，
    def mousePressEvent(self, event):
        self.is_press = True
        self.lastpos = event.pos()
        self.xlist.append(list())
        self.ylist.append(list())

    # 左クリックを離したとき，
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_press:
            self.is_press = False
            self.drawLine(event.pos())
            self.count = self.count + 1
            self.oneline_fin.emit()

            if self.count == self.kakusu:
                self.moji_fin.emit()
                # self.clear()

    # マウスを動かしたとき，
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_press:
            self.drawLine(event.pos())

    # 線を引きます
    def drawLine(self, endpos):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastpos, endpos)
        self.lastpos = QPoint(endpos)
        self.xlist[self.count].append(self.lastpos.x())
        self.ylist[self.count].append(self.lastpos.y())
        # print(self.xlist)
        self.update()

    # x,y座標，画数，描画エリアすべてリセット
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
        #self.input = InputData("data/input.json")
        self.input = InputData("data/num.json")
        #self.text = ["あ", "い", "う", "え", "お"]
        #self.kakusu = [3, 2, 2, 2, 3]
        self.text = self.input.get_all_keydata('text')
        self.kakusu = self.input.get_all_keydata('kakusu')
        self.count = 0
        self.font_scale = QFont()
        self.db = Database()
        self.db.get_json("data/output.json")
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.show()
        self.setWindowLayout()

    def setWindowLayout(self):
        self.order_label = QLabel()
        self.kakusu_label = QLabel()
        self.nokori_label = QLabel()
        self.canvas = Canvas()
        self.nextbtn = QPushButton()
        self.cancelbtn = QPushButton()
        self.skipbtn = QPushButton()
        self.layout = QVBoxLayout()
        self.btnlayout = QHBoxLayout()
        self.nokori_label.setText("残り:"+str(len(self.text)-self.count-1)+"文字")
        self.order_label.setText("<font size='7'>「"+self.text[self.count]+"」</font>を書いてください ["+str(self.kakusu[self.count])+"画]")
        #self.order_label.setText(self.input.data[self.count]['text']+"を書いてください"+str(self.input.data[self.count]['kakusu'])+"画")
        self.kakusu_label.setText("現在 "+str(self.canvas.count)+"/"+str(self.kakusu[self.count]))
        self.canvas.setKakusu(self.kakusu[self.count])
        #self.canvas.kakusu = (self.kakusu[self.count])
        self.canvas.moji_fin.connect(self.dis_paint)
        #self.canvas.oneline_fin.connect(self.update_label)
        self.canvas.oneline_fin.connect(self.label_update)
        self.nextbtn.clicked.connect(self.next_moji)
        self.skipbtn.clicked.connect(self.skip_moji)
        self.cancelbtn.clicked.connect(self.cancel_moji)
        self.canvas.setStyleSheet("background-color:#444444")
        self.cancelbtn.setText("取り消し")
        self.nextbtn.setText("次へ")
        self.skipbtn.setText("スキップ")
        self.btnlayout.addWidget(self.cancelbtn)
        self.btnlayout.addWidget(self.skipbtn)
        self.btnlayout.addWidget(self.nextbtn)
        self.layout.addWidget(self.nokori_label)
        self.layout.addWidget(self.order_label)
        self.layout.addWidget(self.kakusu_label)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.btnlayout)
        self.setLayout(self.layout)
        self.font_scale.setPixelSize(20)
        self.setFont(self.font_scale)

    # 一文字全て書き終わったら
    @Slot()
    def dis_paint(self):
        self.canvas.setEnabled(False)
        # self.canvas.clear()
        # self.field_update()

    def field_update(self):
        #if self.count + 1 < len(self.text):
        #if self.count + 1 < len(self.input.data):
            #self.count = self.count + 1
        self.count = self.count+1
        if self.count  > len(self.input.data):
            self.count = self.count - 1 
        try:
            self.label_update()
            self.canvas.setKakusu(self.kakusu[self.count])
        except IndexError:
            self.canvas.setKakusu(0)
            self.canvas.setEnabled(False)
        #self.canvas.kakusu = (self.kakusu[self.count])
        self.update()

    # 一画書き終わるごと
    @Slot()
    def label_update(self):
        try:
            self.nokori_label.setText("残り:"+str(len(self.text)-self.count-1)+"文字")
            #self.order_label.setText(self.text[self.count]+"を書いてください ["+str(self.kakusu[self.count])+"画]")
            self.order_label.setText("<font size='7'>「"+self.text[self.count]+"」</font>を書いてください ["+str(self.kakusu[self.count])+"画]")
            #self.order_label.setText(self.input.data[self.count]['text']+"を書いてください"+str(self.input.data[self.count]['kakusu'])+"画")
            self.kakusu_label.setText("現在 " + str(self.canvas.count) + "/" + str(self.kakusu[self.count]))
        except IndexError:
            #self.order_label.setText(" "+"を書いてください"+str(0)+"画")
            self.order_label.setText("<font size='7'>「 」</font>を書いてください ["+str(0)+"画]")
            #self.order_label.setText(self.input.data[self.count]['text']+"を書いてください"+str(self.input.data[self.count]['kakusu'])+"画")
            self.kakusu_label.setText("現在 " + str(0) + "/" + str(0))
            self.canvas.setEnabled(False)


    # IndexError解消しろ
    # 文字を取り消し，
    @Slot()
    def cancel_moji(self) -> bool:
        self.canvas.clear()
        self.canvas.setEnabled(True)
        self.label_update()
        self.update()
        return True

    # 次の文字へ
    @Slot()
    def next_moji(self) -> bool:
        if self.kakusu[self.count] != self.canvas.count:
            QMessageBox.information(None,'error','規定画数に達していません',QMessageBox.Ok)
            return False
        self.save_data()
        self.canvas.clear()
        self.canvas.setEnabled(True)
        self.field_update()
        if self.count >= len(self.text):
            QMessageBox.information(None,'お疲れ様でした','すべての文字を書き終えました．',QMessageBox.Ok)
            self.canvas.setEnabled(False)
        print(self.count)
        print(len(self.text))
        return True

    # めんどくさい場合のスキップボタン
    @Slot()
    def skip_moji(self):
        self.canvas.clear()
        self.canvas.setEnabled(True)
        self.field_update()
        if self.count >= len(self.text):
            QMessageBox.information(None,'お疲れ様でした','すべての文字を書き終えました．',QMessageBox.Ok)
            self.canvas.setEnabled(False)
        return True


    # 文字の点列データをjson形式で保存
    def save_data(self):
        print('count==' + str(self.canvas.count))
        plt.xlim(0, self.canvas.canvas_width)
        plt.ylim(self.canvas.canvas_height, 0)
        for i in range(len(self.canvas.xlist)):
            plt.plot(self.canvas.xlist[i], self.canvas.ylist[i])
            print(str(i + 1) + '画目' + str(len(self.canvas.xlist[i])) + ' ' + str(len(self.canvas.ylist[i])))
        tmp = {self.text[self.count]: {"data": {"x": self.canvas.xlist, "y": self.canvas.ylist, "min_x":self.minlist(self.canvas.xlist),"min_y":self.minlist(self.canvas.ylist), "max_x":self.maxlist(self.canvas.xlist), "max_y":self.maxlist(self.canvas.ylist)}}}
        json.dumps(tmp)
        #with open('data/test.json', 'a') as f:
            # with open('data/test.json', 'w') as f:
            #json.dump(tmp, f, indent=4)
        self.db.addData(self.text[self.count],self.canvas.xlist,self.canvas.ylist)
        #self.db.addData(self.input.data[self.count]['text'],self.canvas.xlist,self.canvas.ylist)
        self.db.normalize(self.text[self.count])
        self.db.save_to_json()
        plt.show()

    def minlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(min(i))

        return ans

    def maxlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(max(i))

        return ans

    def keyPressEvent(self, event):
        #print(event.key())
        if event.key() == Qt.Key_Return:
            self.next_moji()
        elif event.key() == 65:
            self.cancel_moji()
        elif event.key() == 83:
            self.skip_moji()

# 平均化の進捗表示用窓
class AverageWindow(QWidget):
    def __init__(self):
        super().__init__()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
