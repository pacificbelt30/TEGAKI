import math
import matplotlib.pyplot as plt

# 余弦フーリエクラス


class cosFourier:
    def __init__(self):
        self._coefficient: list = list()  # 係数
        self._period: float = 2*math.pi  # 周期の1/2
        self._num: int = 1000  # 要素数
        self._limit: int = 100  # フーリエ打ち切り次数

    @property
    def coefficient(self) -> list:
        return self._coefficient

    @coefficient.setter
    def coefficient(self, coefficient):
        self._coefficient = coefficient

    @property
    def period(self) -> float:
        return self._period

    @property
    def num(self) -> int:
        return self._num

    @property
    def limit(self) -> int:
        return self._limit

    # フーリエ級数
    def fourier(self, y: list) -> list:
        time: float = self.period/self.num  # 1区間あたりの長さ
        coe: int = self.an(y)  # an n=50まで
        ans: list = [0]*self.num  # フーリエ級数の各次数の係数 self.num個
        for i in range(self.num):
            ans[i] = ans[i] + coe[0]/2.0
            for j in range(self.limit-1):
                ans[i] = ans[i] + coe[j+1]*math.cos((j+1)/2.0*i*time)

        # print(ans)
        return ans

    # フーリエ級数
    def fourier_M(self, y: list) -> list:
        time: float = self.period / len(y)  # 1区間あたりの長さ
        coea: int = self.an(y)  # an n=50まで
        coeb: int = self.bn(y)  # an n=50まで
        ans: list = [0] * len(y)  # フーリエ級数の各次数の係数 self.num個
        for i in range(len(y)):
            ans[i] = ans[i] + coea[0] / 2.0
            for n in range(self.limit - 1):
                #ans[i] = ans[i] + coea[n + 1] * math.cos((n + 1) / 2.0 * i * time)
                #ans[i] = ans[i] + coea[n + 1] * math.cos((n + 1)* i * 2.0 * math.pi / self.period)
                # ans[i] = ans[i] + coea[n + 1] * math.cos((n + 1) / 2.0 * i * time) + coeb[n + 1] * math.sin((n + 1) / 2.0 * i * time)
                ans[i] = ans[i] + coea[n + 1] * math.cos((n + 1) * i * 2 * math.pi *time/ self.period) + coeb[n + 1] * math.sin((n + 1) * i * 2 * math.pi *time/ self.period)
                # ans[i] = ans[i] + coea[n + 1] * math.cos((n + 1) * i * 2 * math.pi *time/ self.period)

        # print(ans)
        return ans

    # 余弦フーリエのみなのでanのみを求めるだけで良い
    def an(self, y: list) -> list:
        coe: float = 2.0/self.period  # anの積分の係数
        length: int = len(y)  # 入力の長さ
        ans: list = [0]*self.limit  # anの長さはself.limit
        time: float = self.period/length  # 1区間あたりの長さ
        for k in range(self.limit):
            for i in range(length-1):
                x0 = time*i
                x1 = time*(i+1)
                #ans[k] = ans[k] + (y[i]+y[i+1])*time/2.0*math.cos(k/2.0*i*time)
                # ans[k] = ans[k] + (y[i]* math.cos(k / 2.0 * i * time) + y[i + 1]* math.cos(k / 2.0 * (i+1) * time)) * time / 2.0
                ans[k] = ans[k] + (y[i] * math.cos(2 * math.pi * k * x0/ self.period) + y[i + 1] * math.cos(2 * math.pi * k * x1 / self.period)) * time / 2.0
                # ans[k] = ans[k] + (y[i] * math.cos(k/2.0*i*time) + y[i + 1] * math.cos(k/2.0*(i+1)*time)) * time / 2.0
            ans[k] = ans[k]*coe  # 係数割
        #print("DEBUG ans")
        # print(ans)
        return ans

    def bn(self, y: list) -> list:
        coe: float = 2.0/self.period  # bnの積分の係数
        length: int = len(y)  # 入力の長さ
        ans: list = [0]*self.limit  # bnの長さはself.limit
        time: float = self.period/length  # 1区間あたりの長さ
        for k in range(self.limit):
            for i in range(length-1):
                x0 = time*i
                x1 = time*(i+1)
                # ans[k] = ans[k] + (y[i]*math.sin(k/2.0*i*time)+y[i+1]*math.sin(k/2.0*(i+1)*time))*time/2.0
                # ans[k] = ans[k] + (y[i] * math.sin(2 * math.pi * k * i *time/ self.period) + y[i + 1] * math.sin(2 * math.pi * k * (i+1) *time / self.period)) * time / 2.0
                ans[k] = ans[k] + (y[i] * math.sin(2 * math.pi * k * x0/ self.period) + y[i + 1] * math.sin(2 * math.pi * k * x1 / self.period)) * time / 2.0
                # ans[k] = ans[k] + (y[i] * math.sin(k/2.0*i*time) + y[i + 1] * math.sin(k/2.0*(i+1)*time)) * time / 2.0
            ans[k] = ans[k]*coe  # 係数割
        #print("DEBUG ans")
        # print(ans)
        return ans

    # def calc_fourier(self,y:list) -> list:

    # DEBUG プロットする
    def plot(self, y: list):
        time = self.period/len(y)
        print(time)
        tmp = list()
        plt.xlim(0, 2*self.period)
        plt.ylim(-2*self.period, 2*self.period)
        for i in range(len(y)):
            tmp.append(i*self.period/len(y))
        plt.plot(tmp, y)

        # a = self.fourier(y)
        a = self.fourier_M(y)
        print(a)
        tmp = list()
        for i in range(len(y)):
            tmp.append(i*time)
            # print(str(i*time)+","+str(a[i]))
        plt.plot(tmp, a)
        plt.show()
