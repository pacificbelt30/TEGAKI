from dataquery import *
from fourier import *
from spline import *
# 仕様
# 'key':{'yomi':str,'kakusu':int,'x':list,'y':list,'min_x':list,'min_y':list,'max_x':list,'max_y':list}


class Averaging:
    def __init__(self):
        self._moji_file = Database()
        self._moji = dict()
        self._moji_filename = "../data/output/moji.json"
        self._moji_file.get_json(self._moji_filename)
        self._data = Database()
        self._data.get_json("../data/output/output.json")
        self._key_list = self.data.data.keys() # 全鍵のリスト
        self.var_init()

    @property
    def data(self) -> Database:
        return self._data
    @property
    def min_ave(self) -> list:
        return self._min_ave
    @property
    def max_ave(self) -> list:
        return self._max_ave
    @property
    def key_list(self) -> list:
        return self._key_list
    @property
    def max_min_list(self) -> list:
        return self._max_min_list

    def normalize(self): # 正規化
        return True

    def averaging(self): # 平均化
        print("平均化開始")
        for key in self.key_list:
            self.get_max_min_list(key)
            print("key = "+key+", kakusu = "+str(self.data.data[key]['kakusu']))
            tmp = self.data.data[key]
            ave = list() # xとyのmin,maxの配列 min_x,min_y,max_x,max_y -> 0,1,2,3
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['min_x']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['min_y']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['max_x']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['max_y']))
            # keyの文字データを作成
            self._moji[key] = {'yomi':tmp['yomi'],'kakusu':tmp['kakusu'],'x':self.x_average_sp(key),'y':self.y_average_sp(key),'min_x':ave[0],'min_y':ave[1],'max_x':ave[2],'max_y':ave[3]}
            self.var_init() # 初期化
        # 保存
        #print("DEBUG moji = "+str(self._moji))
        self._moji_file.data = self._moji
        self._moji_file.save_to_json()

    # 文字key の xとyの平均化関数(全画)
    def x_average(self,key:str) -> list:
        fourier = cosFourier()
        datakey = 'normdata'
        datakey = 'data'
        ans = [[0]*fourier.num for i in range(self.data.data[key]['kakusu'])]
        coe = 1/len(self.data.data[key][datakey])
        print(key + " x coe:"+str(coe))
        for i in range(len(self.data.data[key][datakey])):
            for j in range(self.data.data[key]['kakusu']):
                tmp = fourier.fourier_M(self.data.data[key][datakey][i]['x'][j])
                for k in range(len(tmp)):
                    try:
                        ans[j][k] = ans[j][k] + coe*tmp[k]
                    except IndexError:
                        print(str(len(ans))+","+str(len(ans[j]))+","+str(j)+","+str(k))
        return ans

    def y_average(self,key:str) -> list:
        fourier = cosFourier()
        datakey = 'normdata'
        datakey = 'data'
        ans = [[0]* fourier.num for i in range(self.data.data[key]['kakusu'])]
        coe = 1/len(self.data.data[key][datakey])
        print(key + " y coe:"+str(coe))
        for i in range(len(self.data.data[key][datakey])):
            for j in range(self.data.data[key]['kakusu']):
                tmp = fourier.fourier_M(self.data.data[key][datakey][i]['y'][j])
                print(self.data.data[key][datakey][i]['y'][j])
                print(tmp)
                for k in range(len(tmp)):
                    try:
                        ans[j][k] = ans[j][k] + coe*tmp[k]
                    except IndexError:
                        print(str(len(ans))+","+str(len(ans[j]))+","+str(j)+","+str(k))
        return ans

    def x_average_sp(self,key:str) -> list:
        spline = Spline()
        datakey = 'normdata'
        #datakey = 'data'
        ans = [[0]*spline.num for i in range(self.data.data[key]['kakusu'])]
        coe = 1/len(self.data.data[key][datakey])
        print(key + " x coe:"+str(coe))
        for i in range(len(self.data.data[key][datakey])):
            for j in range(self.data.data[key]['kakusu']):
                tmp = spline.spline(self.data.data[key][datakey][i]['x'][j])
                for k in range(len(tmp)):
                    try:
                        ans[j][k] = ans[j][k] + coe*tmp[k]
                    except IndexError:
                        print(str(len(ans))+","+str(len(ans[j]))+","+str(j)+","+str(k))
        return ans

    def y_average_sp(self,key:str) -> list:
        spline = Spline()
        datakey = 'normdata'
        #datakey = 'data'
        ans = [[0]*spline.num for i in range(self.data.data[key]['kakusu'])]
        coe = 1/len(self.data.data[key][datakey])
        print(key + " y coe:"+str(coe))
        for i in range(len(self.data.data[key][datakey])):
            for j in range(self.data.data[key]['kakusu']):
                tmp = spline.spline(self.data.data[key][datakey][i]['y'][j])
                for k in range(len(tmp)):
                    try:
                        ans[j][k] = ans[j][k] + coe*tmp[k]
                    except IndexError:
                        print(str(len(ans))+","+str(len(ans[j]))+","+str(j)+","+str(k))
        return ans

    def var_init(self): # 変数初期化
        self._min_ave = list()
        self._max_ave = list()
        self._max_min_list = dict()
        self._max_min_list['min_x'] = list()
        self._max_min_list['min_y'] = list()
        self._max_min_list['max_x'] = list()
        self._max_min_list['max_y'] = list()

    def ave_list(self,kakusu:int,x:list) -> list:
        ans = list()
        for i in range(kakusu):
            tmp = 0
            for j in range(len(x)):
                try:
                    tmp = tmp + x[j][i]
                    # tmp = tmp + x[i][j]
                except IndexError:
                    print("DEBUG INDEXERROR:"+str(i)+","+str(j)+","+str(len(x))+","+str(x))
            ans.append(tmp/len(x))
        return ans

    def get_max_min_list(self,key:str)->list:
        for d in self.data.data[key]['data']:
            self._max_min_list['min_x'].append(d['min_x'])
            self._max_min_list['min_y'].append(d['min_y'])
            self._max_min_list['max_x'].append(d['max_x'])
            self._max_min_list['max_y'].append(d['max_y'])
