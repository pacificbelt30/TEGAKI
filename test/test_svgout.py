#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
sys.path.append('../')
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *
from PySide2.QtWidgets import *
from dataquery import *
from svgout import *

x = [[22, 23, 26, 28, 32, 36, 39, 42, 50, 55, 61, 67, 70, 72, 73, 74],
     [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 48, 49, 49, 50, 51, 51, 52, 53, 56, 57, 58, 58,
      59, 62, 63, 64],
     [64, 64, 64, 64, 64, 63, 62, 61, 59, 58, 57, 56, 55, 54, 52, 51, 49, 46, 45, 43, 41, 40, 39, 38, 37, 37, 37, 37,
      37, 37, 37, 37, 37, 38, 40, 41, 42, 43, 45, 46, 50, 52, 53, 55, 57, 58, 61, 64, 67, 69, 71, 73, 73, 74, 74, 74,
      75, 75, 76, 76, 76, 76, 76]]
y = [[53, 53, 53, 53, 53, 53, 52, 51, 49, 47, 45, 45, 45, 45, 45, 45],
     [43, 45, 46, 47, 50, 51, 53, 58, 61, 62, 64, 65, 67, 68, 69, 70, 71, 73, 74, 75, 75, 76, 77, 78, 80, 81, 81, 82,
      82, 83, 83, 83],
     [73, 74, 77, 78, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 78, 78, 78, 76, 74, 73, 72, 71,
      70, 68, 67, 66, 64, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 63, 64, 65, 67, 69, 71, 72, 73, 74, 75,
      76, 78, 79, 80, 81, 82, 83]]
# x = [[7.60533665101427, -0.032640484946633706, 0.39330656762589994, -0.01625823822959177, 0.4570356002141538,
#       -0.0016853861054703448, 0.4264586977237989, 0.12832724607715645, 1.1213519367413205, -0.44283363134892967,
#       1.2325314101991673, -0.18719068636352146, 0.13973508199216125, -0.19813904638803878, 0.10382425068148247,
#       -0.2331239495008923, -0.2803389526863933, 0.8545823966293656, 0.47477207291271634, 0.05740322714743748,
#       1.2480491840371217, 0.018399849983638784, 0.0732970004035664, 0.19387487609170195, 0.1421681544730263,
#       5.240447856823588, 0.17571261139736566, 0.2905745808927329, 0.12436577904320714, 0.16520125380396777,
#       1.418019006706127, 0.4020299593501895, 1.2322469718715945, 4.042319413979121, -2.117091464483249,
#       -0.9282666539033257, -0.48308619414564863, -0.6281306531917302, -0.4704195296765932, -0.49891802773678734,
#       0.5542968027402746, -0.2826725924383402, 1.011685907101779, 0.10982613413011677, 0.006492053285302658,
#       0.0028072465320002175, -0.12650334865674964, -0.1123120534701135, -0.14122558526124868, -0.11130165278237941,
#       5.440747703518415, -0.10202644004783346, -0.1319957857247132, -0.08515432923709663, -0.08273877944582111,
#       0.07857471077293615, 0.06035835662069734, 0.27365208762361326, 1.508123732688885, -0.05374711006721548,
#       0.4685993140926806, -0.45248556405531876, -0.382452861671353, -0.6923351988603892, -0.16688731793849815,
#       -0.5393831568602396, -1.4126018944800418, 3.0093162843320944, 1.5062550768430163, 0.2864549920878176,
#       1.3518174531183165, -0.05397688158302282, -0.036479285489506866, 0.8507550785028691, 0.33313702160381325,
#       3.782728565177488, 0.3275762907458768, 0.8455830057040499, -0.06923188772148861, -0.12610027578125826,
#       2.3903504742113446, 0.18102526657904933, 1.1885256859231688, 1.5238723164187, -0.5175086183281294,
#       -0.06036264403427205, 0.09431408935055298, -0.4813910127881893, -0.027442135180020484, -0.10055052106491226,
#       0.7177359246255441, 0.4328669813385394, 1.0747412458346814, 0.32075048295470043, 0.017173849997081013,
#       0.08611211623577482, 0.3276334141282099, 0.11321873966502957, -0.09796771521276926, -0.010717948100224469]]
# y = [[3.509020285178964, -0.19826795498423375, -0.19852387336111968, -0.1996706083013144, -0.19107253312313047,
#       -0.19964575138278262, -0.1876949685243828, -0.19168641593990612, -0.13629466997587242, -0.21645985672025503,
#       0.2534169124084414, -0.20432386349890203, -0.14158786795368708, -0.22237376500084471, -0.13710841990504868,
#       -0.21167094063424924, -0.15768750322249994, -0.05169311417679253, -0.01985531296221385, -0.1585769067630957,
#       0.9158443810944412, -0.19652387170281116, -0.02636423188229407, -0.13070200784250421, 0.011927443956312442,
#       3.5320587653437747, 0.031856141372561236, -0.09680733861135779, 0.027742488140252028, -0.18652408657332514,
#       1.2672925322631967, -0.07746301524542692, 0.2809245125993867, 0.5486069055289612, -0.32827902878943593,
#       -0.3121565150984486, -0.05642083908492489, -0.38894356223155935, -0.024137378796879466, -0.3044381970933392,
#       1.2449632073289305, -0.5081339233622135, 1.2365190188766946, 0.13369496392608207, 0.21223759928328678,
#       -0.049846959588410775, 0.2805854489555428, -0.08195717753900125, 0.12906105166477108, -0.10590953900933081,
#       11.479243724109601, -0.10146428914654054, 0.14549873365698113, -0.06138926856532197, 0.35605884999803966,
#       0.010877112317292104, 0.3213613733887548, 0.2660189325315178, 1.7742914130146024, -0.30212034391820497,
#       1.7244741272823847, -0.3480915090081248, 0.06953633787151348, -0.5826301705585665, 0.16403861149942223,
#       -0.27800408068469956, -0.3619957606518037, 1.2736530250555982, 1.1209142228750977, 0.0834880545006765,
#       2.487702394726443, -0.26459596605388896, 0.15996113092544234, 0.6418566133320404, 0.5064750715306789,
#       6.2904636200033455, 0.5189206413928739, 0.7115268963951386, 0.14645447200880915, -0.28544190100761657,
#       2.627011361950635, 0.09822776813200577, 1.381942907819998, 1.3696720005799234, -0.267936404208601,
#       -0.16638971460952776, 0.31759717138499466, -0.6234260631006571, 0.22780706319805058, -0.21976822888562242,
#       0.9483851276636066, 0.2939006420881883, 1.322281735266458, 0.18704365725306016, 0.25041398305838897,
#       -0.055093165230699764, 0.5651911898374186, -0.03191423267814064, -0.05602619120323912, -0.16084765326568667]]
# x = [ 279, 279, 279, 279, 279, 271, 258, 239, 215, 199, 179, 171, 170, 183, 201, 219, 228, 234, 237, 237 ]
# y = [ 215, 222, 230, 284, 310, 326, 338, 349, 364, 386, 421, 427, 428, 428, 425, 418, 414, 412, 412, 412 ]
# x =           [ 261, 261, 262, 264, 266, 268, 270, 271, 273, 278, 284, 287, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290 ]
# y =           [ 153, 154, 156, 157, 159, 162, 169, 181, 200, 218, 237, 272, 306, 331, 335, 336, 368, 393, 403, 408, 409, 409 ]
print("start debug")
app = QApplication(sys.argv)
svg_gen = QSvgGenerator()
svg_gen.setFileName("svg.svg")
svg_gen.setSize(QSize(500, 500))
svg_gen.setViewBox(QRect(0, 0, 500, 500))
svg_gen.setTitle("echo あ")
svg_gen.setDescription("from pyqt QtSvg test.")

painter = QPainter()
painter.begin(svg_gen)
painter.setPen(Qt.black)

rect = QRect(0, 0, 500, 500)
painter.fillRect(rect, Qt.white)

# painter.setPen(Qt.blue)
# painter.setFont(QFont("Arial", 30))
# painter.drawText(rect, Qt.AlignCenter, "Hello SVG")
for i in range(len(x)):
    for j in range(len(x[i]) - 1):
        painter.drawLine(x[i][j]*5,y[i][j]*5,x[i][j+1]*5,y[i][j+1]*5)
        # painter.drawLine(x[i][j] * 50, y[i][j] * 50, x[i][j + 1] * 50, y[i][j + 1] * 50)

# for i in range(len(x)-1):
# print(len(x))
# painter.drawLine(int(x[i]),int(y[i]),int(x[i+1]),int(y[i+1]))
painter.end()

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


class MainWindow(QWidget):
    def __init__(self, parent=None, window=None):
        super(MainWindow, self).__init__()
        self.window_width = 1000
        self.window_height = 1000
        self.setGeometry(100,100,1000,1000)
        self.setFixedSize(self.window_width,self.window_height)
        # self.view = QGraphicsView()
        self.view = SVGView()
        self.scene = QGraphicsScene()
        self.rect = QRect(0,0,500,500)
        # self.svg = QGraphicsSvgItem("test.svg")
        self.svg = QGraphicsSvgItem("svg.svg")
        self.image = QImage("test.png")
        self.pix = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        # self.scene.setSceneRect(rect)
        self.fill_background()
        self.scene.addItem(self.svg)
        # self.scene.addItem(self.pix)
        # self.scene.addRect(rect,QPen(Qt.transparent),QBrush(Qt.yellow))
        # self.view.scale(0.2,0.2)  # scaling
        self.view.setScene(self.scene)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

    def fill_background(self):
        self.view.setBackgroundBrush(Qt.gray)
        # self.scene.setBackgroundBrush(Qt.gray)


#ex = MainWindow()
#ex.show()
#sys.exit(app.exec_())
print("end debug")

print("a4")

a4 = A4_svgenerator()
a4._text = "1234123412341234123412341234123412341234123412341234123412341234\n44444444\n5555555555555555555555555555555555555\nああああああいいいいいうううううえええええおおおおお"
a4.mojidata['1'] = a4.database.data['1']['data'][0]
a4.mojidata['2'] = a4.database.data['2']['data'][0]
a4.mojidata['3'] = a4.database.data['3']['data'][0]
a4.mojidata['4'] = a4.database.data['4']['data'][0]
a4.mojidata['5'] = a4.database.data['5']['data'][0]
a4.mojidata['あ'] = a4.database.data['あ']['data'][0]
a4.mojidata['い'] = a4.database.data['い']['data'][0]
a4.mojidata['う'] = a4.database.data['う']['data'][0]
a4.mojidata['え'] = a4.database.data['え']['data'][0]
a4.mojidata['お'] = a4.database.data['お']['data'][0]
a4.gen()
print(a4._text)
print(len(a4._text))
