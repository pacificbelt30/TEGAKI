import sys
import random
sys.path.append('../')
from averaging import *
from dataquery import *

g = [[0] * 10 for i in range(4)]
g = [[1,2]]
print(g)
print(len(g))
print("Average関数")
a = Averaging()
print(a.max_min_list)
a.get_max_min_list("2")
print(a.max_min_list)
print(a.ave_list(2,a.max_min_list['min_x']))
print(a.ave_list(2,a.max_min_list['max_y']))
a.averaging()
b = Database()
b.get_json("../data/moji.json")
plt.plot(b.data['2']['x'][0],b.data['2']['y'][0])
plt.plot(b.data['あ']['x'][0],b.data['あ']['y'][0])
plt.show()
#print("DEBUG "+str(b.data))
