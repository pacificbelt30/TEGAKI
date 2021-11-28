import sys
import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *
from PySide2.QtWidgets import *


class SVGView(QGraphicsView):
    def __init__(self):
        super(SVGView, self).__init__()
        self.ratio = 1.0
        self.count = 20
        self.is_press:bool = False
        self.pos = QPointF()
        self.lastpos = 0
        self.upperlimit = 100
        self.lowerlimit = 1
        # self.setAcceptDrops(True)

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

    def mousePressEvent(self, event):
        self.is_press = True
        self.lastpos = event.pos()
        print("mousePressEvent")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_press:
            self.is_press = False
            # self.pos.setX(self.pos.x() - (event.pos().x()-self.lastpos.x())/self.ratio)
            # self.pos.setY(self.pos.y() - (event.pos().y()-self.lastpos.y())/self.ratio)
            self.pos.setX(self.pos.x() - (event.pos().x()-self.lastpos.x()))
            self.pos.setY(self.pos.y() - (event.pos().y()-self.lastpos.y()))
            if self.pos.x() < 0:self.pos.setX(0)
            if self.pos.y() < 0:self.pos.setY(0)
            if self.pos.x() > self.sceneRect().width():self.pos.setX(self.sceneRect().width())
            if self.pos.y() > self.sceneRect().height():self.pos.setY(self.sceneRect().height())
            print(self.horizontalScrollBar().setValue(10))

            self.centerOn(self.pos)
            print("mouseReleaseEvent")
            print(self.pos)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_press:
            self.pos.setX(self.pos.x() - (event.pos().x()-self.lastpos.x())/self.ratio)
            self.pos.setY(self.pos.y() - (event.pos().y()-self.lastpos.y())/self.ratio)
            #self.pos.setX(self.pos.x() - (event.pos().x()-self.lastpos.x()))
            #self.pos.setY(self.pos.y() - (event.pos().y()-self.lastpos.y()))
            if self.pos.x() < 0:self.pos.setX(0)
            if self.pos.y() < 0:self.pos.setY(0)
            if self.pos.x() > self.sceneRect().width():self.pos.setX(self.sceneRect().width())
            if self.pos.y() > self.sceneRect().height():self.pos.setY(self.sceneRect().height())
            self.centerOn(self.pos)
            print("mouseMoveEvent2")

    def initScale(self):
        self.scale(1.0/self.ratio,1.0/self.ratio)
        self.count = 20
        self.ratio = 1.0


#class MainWindow(QWidget):
class SVMainWindow(QMainWindow):
    def __init__(self, parent=None, window=None):
        super(SVMainWindow, self).__init__()
        self.window_width = 1000
        self.window_height = 1000
        self.setGeometry(100,100,self.window_width,self.window_height)
        #self.setFixedSize(self.window_width,self.window_height)
        # self.view = QGraphicsView()
        # self.view = SVGView()
        # self.scene = QGraphicsScene()
        # self.svg = QGraphicsSvgItem("test/svg.svg")
        self.view:list = list()
        self.scene:list = list()
        self.svg:list = list()
        self.rect = QRect(0,0,500,500)
        self.image = QImage("test/test.png")
        self.pix = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        # self.scene.setSceneRect(rect)
        # self.fill_background(0)
        #self.scene.addItem(self.svg)
        # self.scene.addItem(self.pix)
        # self.scene.addRect(rect,QPen(Qt.transparent),QBrush(Qt.yellow))
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(lambda index:self.tab.removeTab(index))
        # self.view[0].setScene(self.scene[0])
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab)
        # self.layout.addWidget(self.view)
        self.initUI()

        self.widget = QWidget() # QMainWindowの場合
        #self.setLayout(self.layout)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setAcceptDrops(True)

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
        self.OpenSvgFile(fileName)
        return fileName

    def OpenSvgFile(self,fileName:str):
        if fileName == "":
            print("cannot open: file name is empty")
            return ""
        self.view.append(SVGView())
        self.svg.append(QGraphicsSvgItem(fileName))
        self.scene.append(QGraphicsScene())

        if self.svg[len(self.svg)-1].boundingRect().width() == -1 or self.svg[len(self.svg)-1].boundingRect().height() == -1:
            QMessageBox.information(None, 'error', '有効なsvgファイルではありません', QMessageBox.Ok)
            self.svg.pop(len(self.svg)-1)
            return ""

        index = self.tab.addTab(self.view[self.tab.count()],fileName)
        self.fill_background(index)
        self.scene[index].setSceneRect(0,0,self.svg[index].sceneBoundingRect().width(),self.svg[index].sceneBoundingRect().height())
        self.scene[index].clear()
        self.view[index].initScale()
        self.scene[index].addItem(self.svg[index])
        self.view[index].setScene(self.scene[index])
        self.view[index].update()
        self.tab.setCurrentIndex(index)
        print("open:"+fileName)


    def fill_background(self,index:int):
        self.view[index].setBackgroundBrush(Qt.gray)
        # self.scene.setBackgroundBrush(Qt.gray)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        fileName = event.mimeData().urls()
        for i in range(len(fileName)):
            self.OpenSvgFile(fileName[i].toLocalFile())
            print(str(fileName[i].toLocalFile())+":"+str(type(fileName[i].toLocalFile())))
        # self.text = fileName


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SVMainWindow()
    ex.show()
    sys.exit(app.exec_())
