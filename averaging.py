from dataquery import *
# 仕様
# 'key':{'yomi':str,'kakusu':int,'x':list,'y':list,'min_x':list,'min_y':list,'max_x':list,'max_y':list}


class Averaging:
    def __init__(self):
        self._moji_file = Database()
        self._moji = dict()
        self._moji_filename = "../data/moji.json"
        self._moji_file.get_json(self._moji_filename)
        self._min_ave = list()
        self._max_ave = list()
        self._max_min_list = dict()
        self._max_min_list['min_x'] = list()
        self._max_min_list['min_y'] = list()
        self._max_min_list['max_x'] = list()
        self._max_min_list['max_y'] = list()
        self.data = Database()
        self.data.get_json("../data/output.json")
        self._key_list = self.data.data.keys() # 全鍵のリスト
        self.var_init()

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
            print("key = "+key+", kakusu = "+str(self.data.data[key]['kakusu']))
            self.get_max_min_list(key)
            tmp = self.data.data[key]
            ave = list()
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['min_x']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['min_y']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['max_x']))
            ave.append(self.ave_list(tmp['kakusu'],self.max_min_list['max_y']))
            self._moji[key] = {'yomi':tmp['yomi'],'kakusu':tmp['kakusu'],'x':self.x_average(key),'y':self.y_average(key),'min_x':ave[0],'min_y':ave[1],'max_x':ave[2],'max_y':ave[3]}
            self.var_init()
        print("DEBUG moji = "+str(self._moji))
        self._moji_file.data = self._moji
        self._moji_file.save_to_json()

    def x_average(self,key:str) -> list:
        return self.data.data[key]['normdata'][0]['x']

    def y_average(self,key:str) -> list:
        return self.data.data[key]['normdata'][0]['y']

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
                except IndexError:
                    print("DEBUG INDEXERROR"+str(i)+","+str(j)+","+str(len(x)))
            ans.append(tmp/len(x))
        return ans

    def get_max_min_list(self,key:str)->list:
        for d in self.data.data[key]['data']:
            self._max_min_list['min_x'].append(d['min_x'])
            self._max_min_list['min_y'].append(d['min_y'])
            self._max_min_list['max_x'].append(d['max_x'])
            self._max_min_list['max_y'].append(d['max_y'])
