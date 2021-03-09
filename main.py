# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import sys
import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from svgout import *
from svgViewer import SVGView,SVMainWindow
# import sip


# レポート原稿用のテキストエリア
class ReportArea(QTextEdit):
    def __init__(self, parent=None):
        super(ReportArea, self).__init__(parent)
        self.row = 20
        self.column = 30
        self.font_size = 15
        self.line_count = 0
        self.line_word_count = 0
        font = QFont("MS Gothic",10,QFont.Medium)
        font.setFamily('Japanese')
        font.setPointSize(self.font_size)
        font_met = QFontMetrics(font)
        self.setFont(font)
        self.setLineWrapMode(QTextEdit.FixedColumnWidth)  # 文字数での折返し 3
        self.setWordWrapMode(QTextOption.WrapAnywhere)
        # self.setLineWrapMode(3)  # 文字数での折返し 3
        self.setLineWrapColumnOrWidth(self.column)
        self.setFixedHeight(font_met.height()*self.row)
        self.setViewportMargins(font_met.width('x')*3, 0, 0, 0)
        # self.tmp = QTextBlock()
        self.setFontUnderline(True)

    # DEBUG用
    def print_plaintext(self):
        print(self.toPlainText())
        s = self.toPlainText()
        print(s.split('\n'))
        print(self.get_line_count())
        print(self.get_line_word_count())
        print(self.textCursor().position())

    # 全体の行数を取得 self.columnを上回り折り返された部分は新たな行としてカウントする
    def get_line_count(self):
        # count = 0
        text = self.toPlainText().split('\n')
        count = len(text)
        print(len(text))
        for s in text:
            if len(s) % 30 == 0 and len(s) != 0:
                count = count - 1
            count = count + (len(s) // 30)
            # print(len(s))
            # print(s)
        self.line_count = count
        return count

    # 各行の文字数
    def get_line_word_count(self):
        count = []
        for s in self.toPlainText().split('\n'):
            count.append(len(s))
        self.line_word_count = count
        return count

    # self.rowの制限に引っかかる限界の文字数を取得
    def limit_word_count(self):
        count = 0
        mojisu = 0
        text = self.toPlainText().split('\n')
        # count = len(text)
        print(len(text))
        for s in text:
            if len(s) == 0:
                count = count + 1
            elif len(s) % 30 != 0:
                count = count + 1
            count = count + (len(s) // 30)
            if count > self.row:
                return
            # print(len(s))
            # print(s)
        self.line_count = count
        return count

    def txt_input_limit(self):
        if self.get_line_count() > self.row:
            tmp = self.toPlainText()
            tmp = tmp[:]


#class MainWindow(QWidget):
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_InputMethodEnabled)
        self.row_limit_words = 30
        self.font_size = 15
        self.line_count = 0
        self.line_word_count = [0]

        # self.test = QCheckBox('test', self)
        self.textbox = ReportArea()
        self.btn = QPushButton("SVGを出力(test.svg)", self)
        #self.btn.clicked.connect(self.textbox.print_plaintext)
        self.btn.clicked.connect(self.gen_svg)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.textbox)
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.setGeometry(300, 50, 650, 550)
        self.setFixedSize(650, 550) # サイズ変更不可能にした
        self.setWindowTitle('QCheckBox')
        self.initUI()

    def initUI(self):
        self.create_menu_bar()
        
    def create_menu_bar(self):
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        openAct = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.getOpenFileName)
        saveAct = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(self.getSaveFileName)
        saveAsAct = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Save as', self)
        saveAsAct.setShortcut('Ctrl+Shift+S')
        saveAsAct.triggered.connect(self.getSaveAsFileName)
        self.filemenu.addAction(openAct)
        self.filemenu.addAction(saveAct)
        self.filemenu.addAction(saveAsAct)

    def getOpenFileName(self):
        (fileName, selectedFilter) = QFileDialog.getOpenFileName(self,filter="PlainText Files (*.txt)")
        if fileName == "":
            print("cannot open: file name is empty")
        print("open:"+fileName)
        try:
            with open(fileName, 'r') as f:
                txt = f.read()
        except:
            print("FILEOPENERROR")
        self.textbox.setPlainText(txt)
        return fileName

    def getSaveFileName(self):
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(self,filter="PlainText Files (*.txt)")
        print("save:"+fileName)
        return fileName

    def getSaveAsFileName(self):
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(self,filter="PlainText Files (*.txt)")
        print("save as:"+fileName)
        return fileName

    def print_plaintext(self):
        print(self.textbox.toPlainText())
        s = self.textbox.toPlainText()
        print(s.split('\n'))
        print(self.get_line_count())
        print(self.get_line_word_count())

    def gen_svg(self):
        s = self.textbox.toPlainText()
        a4 = A4_svgenerator()
        a4._text = s
        a4.gen()
        #sv = SVMainWindow()
        #sv.svg = QGraphicsSvgItem("test.svg")
        #sv.scene.clear()
        #sv.scene.addItem(sv.svg)
        #sv.view.update()
        #sv.show()

    def get_line_count(self):
        # count = 0
        text = self.textbox.toPlainText().split('\n')
        count = len(text)
        print(len(text))
        for s in text:
            if len(s) % 30 == 0 and len(s) != 0:
                count = count - 1
            count = count + (len(s) // 30)
            # print(len(s))
            # print(s)
        self.line_count = count
        return count

    def get_line_word_count(self):
        count = []
        for s in self.textbox.toPlainText().split('\n'):
            count.append(len(s))
        self.line_word_count = count
        return count


class RepoWindow(QWidget):
    def __init__(self, text, parent=None):
        super(RepoWindow, self).__init__(parent)
        # self.report_area = QTextEdit()
        self.report_area = ReportArea()
        self.a4word = 30
        self.a4row = 20
        self.text = text
        self.report_area.setText(text)

    def cut_a4size(self):
        self.report_area


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        styleFile = os.path.join(
            os.path.dirname(__file__),
            'style.qss'
        )
        with open(styleFile, 'r') as f:
            style = f.read()
    except:
        style = ''
    app.setStyleSheet(style)
    print(style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
