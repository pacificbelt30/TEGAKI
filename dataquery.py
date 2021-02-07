import json
#from icecream import ic

# 入力用のsomething
# [{"id":,"text":,"kakusu":},]
class InputData:
    def __init__(self,filename):
        print('initialize dataQuery')
        self._data:list = self.get_json(filename) # 入力json
        self._length:int = 0 # 一応長さ いらない
    
    @property
    def data(self) -> list:
        return self._data
    #@data.setter
    #def data(self,data:list):
        #self._data = data
    @property
    def length(self) -> int:
        return self._length
    @length.setter
    def length(self,length:int):
        self._length = length

    # 入力用のjsonデータを返す
    def get_json(self,filename:str) -> list:
        try:
            with open(filename) as f:
                data = json.load(f)
                self.length = len(data)
        except FileNotFoundError:
            print(filename+' is not found.')
            self.length = len(list())
            return list()
        return data

    # n番目の要素を取得
    def get_property(self,num:int,key:str):
        print('index:'+str(num)+',search key:'+key)
        try:
            print('the data:'+str(self.data[num][key]))
            return self.data[num][key]
        except KeyError:
            print('key:',key,' is not found.')
            return dict()
        except IndexError:
            print('index:'+str(num)+' is out of range in this data.')

    def get_all_keydata(self,key:str) -> list:
        if key not in self.data[0]:
            print(key+" is not found")
            return list()
        tmp = list()
        for i in self.data:
            tmp.append(i[key])
        return tmp

# データベースとして使いたい予定
# "i":{"id":,"yomi":,"kakusu":,"len":,"datanum":,"data":}
class Database:
    def __init__(self):
        self._data = dict() # データ フォーマット変えたいかもしれない
        self._file:str = "data/output.json" # データベースファイル名
    @property
    def data(self) -> dict:
        return self._data
    #@data.setter
    #def data(self,data:dict):
        #self._data = data
    @property
    def file(self) -> str:
        return self._file
    @file.setter
    def file(self,filename:str):
        self._file = filename

    # 存在しないyomiのデータを作成する
    def create(self,yomi:str,kakusu:int,length:int):
        if yomi not in self.data:
            self.data[yomi] = {'id':len(self.data)+1,'yomi':yomi,'kakusu':kakusu,'len':length,'datanum':0,'data':list()}

    # データを加える
    def addData(self,key:str,x:list,y:list) -> bool:
        if key not in self.data:
            if len(x) != len(y):
                print("長さが違う")
                return False
            self.create(key,len(x),5)
            #return False
        if self.data[key]['kakusu'] != len(x) or self.data[key]['kakusu'] != len(y):
            print("画数が…")
            return False
        #self.data[key]['data'].append({'x':x,'y':y,'min_x'})
        #self.data[key]['data'].append({"data": {"x": x, "y": y, "min_x":self.minlist(x),"min_y":self.minlist(y), "max_x":self.maxlist(x), "max_y":self.maxlist(y)}})
        self.data[key]['data'].append({"x": x, "y": y, "min_x":self.minlist(x),"min_y":self.minlist(y), "max_x":self.maxlist(x), "max_y":self.maxlist(y)})
        self.data[key]['datanum'] = self.data[key]['datanum'] + 1
        return True

    # keyを全消し 要素消しにしたい
    def delete(self,key:str):
        try:
            self.data.pop(key)
        except KeyError:
            print("削除失敗")

    # 正規化したい 
    def normalize(self,key:str):
        tmp = self.data[key]['data'] # 
        tmp2 = dict() # 保存するデータ
        tmp2['normdata'] = list()
        for i in range(len(tmp)):
            tmp2['normdata'].append({'x':list(),'y':list()})
            for j in range(self.data[key]['kakusu']):
                tmp2['normdata'][i]['x'].append(list())
                tmp2['normdata'][i]['y'].append(list())
                maxx = max(tmp[i]['x'][j])
                maxy = max(tmp[i]['y'][j])
                minx = min(tmp[i]['x'][j])
                miny = min(tmp[i]['y'][j])
                # 完全にx軸ory軸に平行な直線の場合，0割発生の可能性がある
                # 0割例外のときはすべて1になる
                for k in tmp[i]['x'][j]:
                    try:
                        tmp2['normdata'][i]['x'][j].append((k-minx)/(maxx-minx))
                    except ZeroDivisionError:
                        tmp2['normdata'][i]['x'][j].append(1)
                for k in tmp[i]['y'][j]:
                    try:
                        tmp2['normdata'][i]['y'][j].append((k-miny)/(maxy-miny))
                    except ZeroDivisionError:
                        tmp2['normdata'][i]['y'][j].append(1)

        self.data[key]['normdata'] = tmp2['normdata']
        print(self.data)

    # json取得 self.dataに格納される
    def get_json(self,filename:str) -> dict:
        self.file = filename
        try:
            with open(filename) as f:
                self._data = json.load(f)
        except FileNotFoundError:
            print(filename+' is not found.')
            return ''
        return self.data

    # listの中の最小値 正規化したデータを戻すときに使うかもしれない
    def minlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(min(i))
        return ans

    # listの中の最大値 正規化したデータを戻すときに使うかもしれない
    def maxlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(max(i))
        return ans

    # 現在のself.dataをjsonとしてself.fileに保存
    def save_to_json(self):
        if self.file == "":
            print("filename was not setting")
            return False
        with open(self.file, 'w') as f:
            # with open('test.json', 'w') as f:
            json.dump(self.data, f, indent=2)
 
    # データの検証 だめな場合は排除？
    def validation(self):
        return True

# t軸0~2piに正規化
# x,y軸0 ~ 1に正規化

