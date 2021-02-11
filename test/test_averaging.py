import sys
import random
sys.path.append('../')
from averaging import *
from dataquery import *

a = Averaging()
print(a.max_min_list)
a.get_max_min_list("5")
print(a.max_min_list)
print(a.ave_list(2,a.max_min_list['min_x']))
print(a.ave_list(2,a.max_min_list['max_y']))
a.averaging()
b = Database()
b.get_json("../data/moji.json")
print("DEBUG "+str(b.data))