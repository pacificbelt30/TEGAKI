import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *
from PySide2.QtWidgets import *


class SVGView(QGraphicsView):
    def __init__(self):
        super(SVGView, self).__init__()
        self.ratio = 1.0
        self.count = 10
        self.upperlimit = 30
        self.lowerlimit = 1

    def wheelEvent(self, event:QWheelEvent):
        if event.delta() >= 0:
            self.count = self.count + 1
            ratio = self.count / (self.count-1)
            if self.count > self.upperlimit:
                self.count = self.upperlimit
                return
            # self.scale(1.1,1.1)
            self.scale(ratio,ratio)
            self.ratio = ratio*(self.count-1)/10
        else:
            self.count = self.count - 1
            ratio = self.count / (self.count+1)
            if self.count < self.lowerlimit:
                self.count = self.lowerlimit
                return
            # self.scale(0.9,0.9)
            self.scale(ratio,ratio)
            self.ratio = ratio*(self.count+1)/10
        print("now ratio :" + str(self.ratio))


#class MainWindow(QWidget):
class MainWindow(QMainWindow):
    def __init__(self, parent=None, window=None):
        super(MainWindow, self).__init__()
        self.window_width = 1000
        self.window_height = 1000
        self.setGeometry(100,100,self.window_width,self.window_height)
        #self.setFixedSize(self.window_width,self.window_height)
        # self.view = QGraphicsView()
        self.view = SVGView()
        self.scene = QGraphicsScene()
        self.rect = QRect(0,0,500,500)
        # self.svg = QGraphicsSvgItem("test.svg")
        self.svg = QGraphicsSvgItem("test/svg.svg")
        self.image = QImage("test/test.png")
        self.pix = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        # self.scene.setSceneRect(rect)
        self.fill_background()
        #self.scene.addItem(self.svg)
        # self.scene.addItem(self.pix)
        # self.scene.addRect(rect,QPen(Qt.transparent),QBrush(Qt.yellow))
        # self.view.scale(0.2,0.2)  # scaling
        self.view.setScene(self.scene)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.initUI()

        self.widget = QWidget() # QMainWindowの場合
        #self.setLayout(self.layout)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


    def initUI(self):
        self.create_menu_bar()

    def create_menu_bar(self):
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        openAct = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.getOpenFileName)
        self.filemenu.addAction(openAct)

    def getOpenFileName(self)->str:
        (fileName, selectedFilter) = QFileDialog.getOpenFileName(self,filter="Image Files (*.svg)")
        if fileName == "":
            print("cannot open: file name is empty")
            return ""
        self.svg = QGraphicsSvgItem(fileName)
        self.scene.clear()
        self.scene.addItem(self.svg)
        self.view.update()
        print("open:"+fileName)
        return fileName

    def fill_background(self):
        self.view.setBackgroundBrush(Qt.gray)
        # self.scene.setBackgroundBrush(Qt.gray)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
