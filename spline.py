import math
from scipy import interpolate
import matplotlib.pyplot as plt


class Spline:
    def __init__(self):
        self._period: float = 2*math.pi
        self._num: int = 100  # 要素数

    @property
    def period(self) -> float:
        return self._period
    @property
    def num(self) -> int:
        return self._num

    def spline(self,x:list) -> list:
        time1: float = self.period / (len(x)-1)
        time2: float = self.period / (self.num-1)
        ans: list = [0] * self.num
        tmp = list()
        for i in range(len(x)):
            tmp.append(i*time1)
        fx = interpolate.interp1d(tmp,x,kind="cubic")
        for i in range(self.num):
            try:
                ans[i] = fx(i*time2)
            except:
                print("DEBUG:"+str(i*time2)+","+str(tmp[len(tmp)-1]))
                print("DEBUG:"+str(i*time2>tmp[len(tmp)-1]))
                ans[i] = fx(tmp[len(tmp)-1])  # 丸め誤差の問題？で例外が出るので緊急手段
        return ans


