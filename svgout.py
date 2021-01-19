#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
#from PySide.QtCore import *
#from PySide.QtGui import *
#from PySide.QtSvg import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsView

class Svgenerator:
    def __init__(self):
        self.svg

x = [[22, 23, 26, 28, 32, 36, 39, 42, 50, 55, 61, 67, 70, 72, 73, 74], [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 48, 49, 49, 50, 51, 51, 52, 53, 56, 57, 58, 58, 59, 62, 63, 64], [64, 64, 64, 64, 64, 63, 62, 61, 59, 58, 57, 56, 55, 54, 52, 51, 49, 46, 45, 43, 41, 40, 39, 38, 37, 37, 37, 37, 37, 37, 37, 37, 37, 38, 40, 41, 42, 43, 45, 46, 50, 52, 53, 55, 57, 58, 61, 64, 67, 69, 71, 73, 73, 74, 74, 74, 75, 75, 76, 76, 76, 76, 76]]
y = [[53, 53, 53, 53, 53, 53, 52, 51, 49, 47, 45, 45, 45, 45, 45, 45], [43, 45, 46, 47, 50, 51, 53, 58, 61, 62, 64, 65, 67, 68, 69, 70, 71, 73, 74, 75, 75, 76, 77, 78, 80, 81, 81, 82, 82, 83, 83, 83], [73, 74, 77, 78, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 78, 78, 78, 76, 74, 73, 72, 71, 70, 68, 67, 66, 64, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 63, 64, 65, 67, 69, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83]]
app = QApplication(sys.argv)
svg_gen = QSvgGenerator()
svg_gen.setFileName("test.svg")
svg_gen.setSize(QSize(200, 200))
svg_gen.setViewBox(QRect(0, 0, 200, 200))
svg_gen.setTitle("echo あ")
svg_gen.setDescription("from pyqt QtSvg test.")


painter = QPainter()
painter.begin(svg_gen)
painter.setPen(Qt.black)


rect = QRect(0, 0, 200, 200)
painter.fillRect(rect, Qt.white)

#painter.setPen(Qt.blue)
#painter.setFont(QFont("Arial", 30))
#painter.drawText(rect, Qt.AlignCenter, "Hello SVG")
for i in range(len(x)):
    for j in range(len(x[i])-1):
        painter.drawLine(x[i][j],y[i][j],x[i][j+1],y[i][j+1])

painter.end()
