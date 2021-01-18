import math
import matplotlib.pyplot as plt

#余弦フーリエクラス
class cosFourier:
    def __init__(self):
        self._coefficient = list() # 係数
        self._period = 2*math.pi # 周期の1/2
        self._num = 100 # 要素数
        self._limit = 50 # フーリエ打ち切り次数

    @property
    def coefficient(self):
        return self._coefficient
    @coefficient.setter
    def coefficient(self,coefficient):
        self._coefficient = coefficient

    @property
    def period(self):
        return self._period
    @property
    def num(self):
        return self._num
    @property
    def limit(self):
        return self._limit

    # フーリエ級数
    def fourier(self,y:list) -> list:
        length = len(y) # 入力の長さ
        time = self.period/self.num # 1区間あたりの長さ
        coe = self.an(y) # an n=50まで
        ans = [0]*self.num # フーリエ級数の各次数の係数 self.num個
        for i in range(self.num):
            ans[i] = ans[i] + coe[0]/2.0
            for j in range(self.limit-1):
                ans[i] = ans[i] + coe[j+1]*math.cos((j+1)/2.0*i*time)

        #print(ans)
        return ans
        

    # 余弦フーリエのみなのでanのみを求めるだけで良い
    def an(self,y:list) -> list:
        coe = 2.0/self.period # anの積分の係数
        length = len(y) # 入力の長さ
        ans = [0]*self.limit # anの長さはself.limit
        time = self.period/length # 1区間あたりの長さ
        for n in range(self.limit):
            for i in range(length-1):
                ans[n] = ans[n] + (y[i]+y[i+1])*time/2.0*math.cos(n/2.0*i*time)
            ans[n] = ans[n]/math.pi
        #print("DEBUG ans")
        #print(ans)
        return ans

    # DEBUG プロットする
    def plot(self,y:list):
        time = self.period/self.num
        print(time)
        tmp = list()
        plt.xlim(0, self.period)
        plt.ylim(-self.period,self.period)
        for i in range(len(y)):
            tmp.append(i*self.period/len(y))
        plt.plot(tmp,y)
        
        a = self.fourier(y)
        print(a)
        tmp = list()
        for i in range(self.num):
            tmp.append(i*time)
            #print(str(i*time)+","+str(a[i]))
        plt.plot(tmp,a)
        plt.show()



        

for a in range(4-1):
    print(a)

x = [0,1,2,3,4,5,6,7,8,9,10]
y = [1,0,-1,0,1,0,-1,0,1,0,-1,0]
y = list()

for i in range(100):
    y.append(math.sin(i*2*math.pi/100))
a = cosFourier()
a.an(y)
a.fourier(y)
a.plot(y)
