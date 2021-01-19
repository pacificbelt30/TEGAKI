
class Averaging:
    def __init__(self):
        self._min_ave = list()
        self._max_ave = list()
        self._key_list = list() # 全鍵のリスト

    @property
    def min_ave(self) -> list:
        return self._min_ave
    @property
    def max_ave(self) -> list:
        return self._max_ave
    @property
    def key_list(self) -> list:
        return self._key_list

    def normalize(self): # 正規化
        return True
    def averaging(self): # 平均化
        return True
    def var_init(self): # 変数初期化
        return True

