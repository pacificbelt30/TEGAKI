import json
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
            return ''
        return self.data

    def get_mojidata(self,moji):
        print('search key:'+moji)
        try:
            return self.data[moji]
        except KeyError:
            print('key:',moji,' is not found.')
            return ''

class database:
    # "i":{"id":,"yomi":,"kakusu":,"len":,"datanum":,"data":}
    def __init__(self):
        self._data = ''
    @property
    def data(self) -> dict:
        return self._data
    @data.setter
    def data(self,data) -> dict:
        self._data = data

    def create(self,yomi:str,kakusu:int,length:int):
        self.data[yomi] = {'id':len(self.data)+1,'yomi':yomi,'kakusu':kakusu,'len':length,'datanum':0,'data':list()}

    def addData(self,key:str,x:list,y:list):
        if key not in self.data:
            #self.create()
            print("不正鍵")
            return ''
        if self.data[key]['kakusu'] != len(x) or self.data[key]['kakusu'] != len(y):
            print("画数が…")
            return ''
        self.data[key]['data'].append({'x':x,'y':y})
        self.data[key]['datanum'] = self.data[key]['datanum'] + 1

    def delete(self,key:str):
        try:
            self.data.pop(key)
        except KeyError:
            print("削除失敗")




a = dataQuery("template.json")
#print(a.get_json('template.json'))
print(a.get_mojidata('あ'))
print(a.get_mojidata('い')['data'])
b = database()
b.data = a.data
print('い' in b.data)
x = [[1,2,3,4,5,6,7],[2,3,4]]
y = [[2,3,4,5,6,7],[2,3,4]]
print(len(x))
print(len(y))
b.addData('い',x,y)
b.create('う',2,5)
b.addData('う',x,y)
print(b.data)
b.delete('い')
b.delete('u')
print(b.data)
