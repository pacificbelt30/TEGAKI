#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *
from PySide2.QtWidgets import *
from dataquery import *
import os
import math


# A罫，B罫で寸法に規格があるわけではなかった
# KOKUYO レ-116A, レ116B
# A4(297x210) A罫 34行7mm，B罫 40行6mm
# ヘッダー 42.5mm + 1mm, フッター 15mm + 0.5mm
#A罫 左 7mm, 右 7mm, 補助線7mmx28
#B罫 左 6mm, 右 6mm, 補助線6mmx35
# textに平文を入れてself.gen()
class A4_svgenerator:
    def __init__(self):
        self._svg: QSvgGenerator = QSvgGenerator()
        #self._title: str = "test.svg"
        self._title: str = "test"
        self._hol:int = 210*100 # 横ピクセル
        self._ver:int = round(self.hol*math.sqrt(2)) # 縦ピクセル
        self._row: int = 34  # 行
        self._column: int = 28  # 列
        self._pixel: int = int(self.hol/30)  # 一文字分のピクセル
        self._head_margin: int = round(43.5/297*self.ver)
        self._bottom_margin: int = self.ver-self.head_margin+self.row*self.pixel
        self._right_margin: int = int(self.hol/30)
        self._left_margin: int = int(self.hol/30)
        self._line_margin: int = int(0)
        self._mojidata: dict = dict()
        self._database: Database = Database()
        self._database.get_json("data/output/moji.json")
        self._mojidata = self.database.data
        self._text: str = ""
        self._page: int = 0

        self.svg.setFileName(self.title)
        # self.svg.setSize(QSize(self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        # self.svg.setViewBox(QRect(0, 0,self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        #self.svg.setSize(QSize(self.column*self.pixel+(self.left_margin+self.right_margin),self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin)))
        #self.svg.setViewBox(QRect(0,0,self.column*self.pixel+(self.left_margin+self.right_margin),self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin)))
        self.svg.setSize(QSize(self.hol,self.ver))
        self.svg.setViewBox(QRect(0,0,self.hol,self.ver))
        # self.svg.setSize(QSize(500,500))
        # self.svg.setViewBox(QRect(0, 0,500,500))
        self.svg.setTitle(self.title)
        self.svg.setDescription("from pySide2 QtSvg.")

    @property
    def ver(self):
        return self._ver

    @property
    def hol(self):
        return self._hol

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

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self,page:int):
        self._page = page

    def gen(self) -> bool:
        self.text = self.trans_han_to_zen(self.text)
        self.page = 0
        fin: int = len(self.text)
        count:int = 0
        if self.text.replace('\n','') == "":
            return False
        while True:
            if count == fin: break
            self.page = self.page + 1
            # self.setSVGConfig(self.title+"_"+str(self.page))
            file = os.path.splitext(self.title)
            print(type(file))
            self.setSVGConfig(file[0]+"_"+str(self.page)+".svg")
            print("page:"+str(self.page))
            painter = QPainter()
            pen = QPen()
            pen.setWidth(5)
            pen.setColor(Qt.black)
            painter.begin(self.svg)
            painter.setPen(pen)
            #rect = QRect(0, 0, self.column * self.pixel + (self.left_margin + self.right_margin),
                                      #self.row * (self.line_margin + self.pixel) + (
                                                  #self.head_margin + self.bottom_margin))
            rect = QRect(0, 0,self.hol,self.ver)
            painter.fillRect(rect, Qt.white)
            i: int = 0
            while True:
                j: int = 0
                if i == self.row: break
                i = i + 1
                while True:
                    if j == self.column or count == fin: break
                    if self.text[count] == '\n':
                        print("return break")
                        count = count + 1
                        break
                    try:
                        self.draw_moji(self.mojidata[self.text[count]],painter,i,j)
                        print(self.mojidata[self.text[count]])
                    except KeyError:
                        import traceback
                        traceback.print_exc()

                    j = j + 1
                    count = count + 1
            painter.end()
        print("DEBUG:count"+str(count))
        return True

    def draw_moji(self,moji:list,painter:QPainter,line:int,row:int):
        top_margin = line*(self.pixel+self.line_margin)+self.head_margin
        left_margin = row*self.pixel+self.left_margin
        for i in range(len(moji['x'])):
            sax = (moji['max_x'][i] - moji['min_x'][i])*self.pixel
            say = (moji['max_y'][i] - moji['min_y'][i])*self.pixel
            for j in range(len(moji['x'][i])-1):
                # print(str(i) + " ," + str(j) + " ," + str(moji['x']) + " ," + str(moji['y']))
                 #painter.drawLine(moji['x'][i][j] * self.pixel, moji['y'][i][j] * self.pixel, moji['x'][i][j + 1] * self.pixel, moji['y'][i][j + 1] * self.pixel)
                # painter.drawLine(moji['x'][i][j],moji['y'][i][j], moji['x'][i][j + 1], moji['y'][i][j + 1])
                #painter.drawLine(left_margin+moji['x'][i][j],top_margin+moji['y'][i][j], left_margin+moji['x'][i][j + 1], top_margin+moji['y'][i][j + 1])
                painter.drawLine(round(left_margin+moji['x'][i][j]*sax+moji['min_x'][i]*self.pixel),round(top_margin+moji['y'][i][j]*say+moji['min_y'][i]*self.pixel), round(left_margin+moji['x'][i][j + 1] *sax+moji['min_x'][i]* self.pixel), round(top_margin+moji['y'][i][j + 1]*say+moji['min_y'][i]* self.pixel))

    def setSVGConfig(self,file:str):
        # self._title = file
        self._svg = QSvgGenerator()
        self.svg.setFileName(file)
        # self.svg.setSize(QSize(self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        # self.svg.setViewBox(QRect(0, 0,self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin),self.column*self.pixel+(self.left_margin+self.right_margin)))
        #self.svg.setSize(QSize(self.column*self.pixel+(self.left_margin+self.right_margin),self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin)))
        #self.svg.setViewBox(QRect(0,0,self.column*self.pixel+(self.left_margin+self.right_margin),self.row*(self.line_margin+self.pixel)+(self.head_margin+self.bottom_margin)))
        self.svg.setSize(QSize(self.hol,self.ver))
        self.svg.setViewBox(QRect(0,0,self.hol,self.ver))
        # self.svg.setSize(QSize(500,500))
        # self.svg.setViewBox(QRect(0, 0,500,500))
        self.svg.setTitle(file)
        self.svg.setDescription("from pySide2 QtSvg.")

    def trans_han_to_zen(self,text:str):
        return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

