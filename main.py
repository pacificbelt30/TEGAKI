# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# import sip


# レポート原稿用のテキストエリア
class ReportArea(QTextEdit):
    def __init__(self, parent=None):
        super(ReportArea, self).__init__(parent)
        self.row = 20
        self.column = 30
        self.font_size = 15
        font = QFont()
        font.setPointSize(self.font_size)
        font_met = QFontMetrics(font)
        self.setFont(font)
        self.setLineWrapMode(3)  # 文字数での折返し
        self.setLineWrapColumnOrWidth(self.row)
        self.setFixedHeight(font_met.height()*self.column)
        self.setViewportMargins(font_met.width('x')*3, 0, 0, 0)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.row_limit_words = 30
        self.font_size = 15
        self.line_count = 0
        self.line_word_count = [0]

        # self.test = QCheckBox('test', self)
        self.btn = QPushButton("BUTTON", self)
        self.btn.clicked.connect(self.print_praintext)
        self.textbox = ReportArea()
        layout = QVBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.textbox)
        self.setGeometry(300, 50, 650, 550)
        self.setWindowTitle('QCheckBox')

    def print_plaintext(self):
        print(self.textbox.toPlainText())
        s = self.textbox.toPlainText()
        print(s.split('\n'))
        print(self.get_line_count())
        print(self.get_line_word_count())

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
        super(MainWindow, self).__init__(parent)
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
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
