from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import sys
import os

args = sys.argv
filename = "./test.svg"
filename_without_ext = os.path.splitext(os.path.basename(filename))[0]

drawing = svg2rlg(filename)
renderPDF.drawToFile(drawing, filename_without_ext + ".pdf")

