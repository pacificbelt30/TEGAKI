import sys
import random
sys.path.append('../')
from fourier import *

length = 500

for a in range(4-1):
    print(a)

x = [0,1,2,3,4,5,6,7,8,9,10]
y = [1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0,1,0,-1,0]
# y = [0,1,2,3,4,3,2,1,1,2,3,2,1,0,1,2,3,4,3,2,1,1,2,3,2,1,0,1,2,3,4,3,2,1,1,2,3,2,1,0,1,2,3,4,3,2,1,1,2,3,2,1,]
# y = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0]
print(type(y))
a = cosFourier()
a.fourier_M(y)
a.plot(y)

y = list()
for i in range(length):
    y.append(9*math.cos(i*2*math.pi/length))
a.an(y)
a.fourier(y)
a.fourier_M(y)
a.plot(y)
y = list()
for i in range(length):
    y.append(4*math.sin(i*2*math.pi/length))
a.fourier_M(y)
a.plot(y)
y = list()
for i in range(length):
    y.append(4*math.cos(i*2*math.pi/length))
a.fourier_M(y)
a.plot(y)

y = list()
for i in range(length):
    y.append(4*math.cos(i*2*math.pi/length)+3-2*math.cos((i+1)*2*math.pi/length))
a.fourier_M(y)
a.plot(y)
