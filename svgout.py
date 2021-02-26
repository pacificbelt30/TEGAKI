#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *
from PySide2.QtWidgets import *
from dataquery import *


class A4_svgenerator:
    def __init__(self):
        self._svg: QSvgGenerator = QSvgGenerator()
        self._title: str = "test.svg"
        self._row: int = 30  # 行
        self._column: int = 30  # 列
        self._pixel: int = 500  # 一文字分のピクセル
        self._head_margin: int = self.pixel*3
        self._bottom_margin: int = self.pixel*3
        self._right_margin: int = self.pixel*3
        self._left_margin: int = self.pixel*3
        self._line_margin: int = int(self.pixel/6)
        self._mojidata: dict = dict()
        self._database: Database = Database()
        self._database.get_json("../data/output.json")
        self._text: str = ""

        self.svg.setFileName(self.title)
        # self.svg.setSize(QSize(self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        # self.svg.setViewBox(QRect(0, 0,self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        self.svg.setSize(QSize(500,500))
        self.svg.setViewBox(QRect(0, 0,500,500))
        self.svg.setTitle(self.title)
        self.svg.setDescription("from pySide2 QtSvg.")

    @property
    def svg(self):
        return self._svg

    @property
    def title(self):
        return self._title

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def pixel(self):
        return self._pixel

    @property
    def head_margin(self):
        return self._head_margin

    @property
    def bottom_margin(self):
        return self._bottom_margin

    @property
    def right_margin(self):
        return self._right_margin

    @property
    def left_margin(self):
        return self._left_margin

    @property
    def line_margin(self):
        return self._line_margin

    @property
    def mojidata(self):
        return self._mojidata

    @property
    def database(self):
        return self._database

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    def gen(self):
        painter = QPainter()
        painter.begin(self.svg)
        painter.setPen(Qt.black)
        # rect = QRect(0, 0,self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*(self.pixel)+(self.left_margin+self.right_margin))
        rect = QRect(0, 0,500,500)
        painter.fillRect(rect, Qt.white)
        fin: int = len(self.text)
        count:int = 0
        i: int = 0
        while True:
            j: int = 0
            if i == self.row: break
            i = i + 1
            while True:
                if j == self.column or count == fin: break
                if self.text[j] == '\n': break
                try:
                    self.draw_moji(self.mojidata[self.text[j]],painter)
                    print(self.mojidata[self.text[j]])
                except KeyError:
                    import traceback
                    traceback.print_exc()

                j = j + 1
                count = count + 1
        painter.end()

    def draw_moji(self,moji:list,painter:QPainter):
        for i in range(len(moji['x'])):
            for j in range(len(moji['x'][i])-1):
                print(str(i) + " ," + str(j) + " ," + str(moji['x']) + " ," + str(moji['y']))
                # painter.drawLine(moji['x'][i][j] * self.pixel, moji['y'][i][j] * self.pixel, moji['x'][i][j + 1] * self.pixel, moji['y'][i][j + 1] * self.pixel)
                painter.drawLine(moji['x'][i][j],moji['y'][i][j], moji['x'][i][j + 1], moji['y'][i][j + 1])
