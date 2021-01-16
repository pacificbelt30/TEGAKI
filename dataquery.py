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

a = dataQuery("template.json")
#print(a.get_json('template.json'))
print(a.get_mojidata('あ'))
print(a.get_mojidata('い'))
