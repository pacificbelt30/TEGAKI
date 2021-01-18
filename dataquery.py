import json
#from icecream import ic
# データベースとして使いたい予定
class dataQuery:
    def __init__(self,filename):
        print('initialize dataQuery')
        self._data = self.get_json(filename)
    
    @property
    def data(self) -> dict:
        return self._data
    @data.setter
    def data(self,data) -> dict:
        self._data = data

    def get_json(self,filename):
        try:
            with open(filename) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(filename+' is not found.')
            return dict()
        return self.data

    def get_mojidata(self,moji):
        print('search key:'+moji)
        try:
            return self.data[moji]
        except KeyError:
            print('key:',moji,' is not found.')
            return dict()

class database:
    # "i":{"id":,"yomi":,"kakusu":,"len":,"datanum":,"data":}
    def __init__(self):
        self._data = dict()
    @property
    def data(self) -> dict:
        return self._data
    @data.setter
    def data(self,data:dict):
        self._data = data

    def create(self,yomi:str,kakusu:int,length:int):
        if yomi not in self.data:
            self.data[yomi] = {'id':len(self.data)+1,'yomi':yomi,'kakusu':kakusu,'len':length,'datanum':0,'data':list()}

    def addData(self,key:str,x:list,y:list):
        if key not in self.data:
            #self.create()
            print("不正鍵")
            return ''
        if self.data[key]['kakusu'] != len(x) or self.data[key]['kakusu'] != len(y):
            print("画数が…")
            return ''
        #self.data[key]['data'].append({'x':x,'y':y,'min_x'})
        self.data[key]['data'].append({"data": {"x": x, "y": y, "min_x":self.minlist(x),"min_y":self.minlist(y), "max_x":self.maxlist(x), "max_y":self.maxlist(y)}})
        self.data[key]['datanum'] = self.data[key]['datanum'] + 1

    def delete(self,key:str):
        try:
            self.data.pop(key)
        except KeyError:
            print("削除失敗")

    def normalize(self,key:str):
        tmp = self.data[key]['data']
        tmp2 = dict()
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
                for k in tmp[i]['x'][j]:
                    tmp2['normdata'][i]['x'][j].append((k-minx)/(maxx-minx))
                for k in tmp[i]['y'][j]:
                    tmp2['normdata'][i]['y'][j].append((k-miny)/(maxy-miny))
        self.data[key]['normdata'] = tmp2['normdata']
        print(self.data)

    def get_json(self,filename:str) -> dict:
        try:
            with open(filename) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(filename+' is not found.')
            return ''
        return self.data

    def minlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(min(i))

        return ans

    def maxlist(self,x:list) -> list:
        ans = list()
        for i in x:
            ans.append(max(i))

        return ans

    def save_to_json(self):
        with open('data/database.json', 'w') as f:
            # with open('test.json', 'w') as f:
            json.dump(self.data, f, indent=2)
 





# t軸0~2piに正規化
# x,y軸0 ~ 1に正規化

a = dataQuery("data/template.json")
#print(a.get_json('template.json'))
print(a.get_mojidata('あ'))
print(a.get_mojidata('い')['data'])
b = database()
#b = database("template.json")
b.get_json("data/database.json")
print('い' in b.data)
x = [[1,2,3,4,5,6,7],[2,3,4]]
y = [[2,3,4,5,6,7],[2,3,4]]
print(len(x))
print(len(y))
b.addData('い',x,y)
b.create('う',2,5)
b.addData('う',x,y)
#print(b.data)
#b.delete('い')
#b.delete('u')
#print(b.data)
b.normalize('あ')
b.addData('う',x,y)
b.save_to_json()
