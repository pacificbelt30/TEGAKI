# TEGAKI
手書き文字を生成し，ディジタル上で手書き文字レポートを作成する
# how to use
environment:
- python (version 3.9.1)
    - pyside2 or pyqt5
    - json
    - matplotlib

install package with pip to run this app:
```bash
pip install -r requirements.txt
```
  
If registry moji data:
```bash
python regmoji.py
```

If write report:
```bash
python main.py
```

If view svg files:
```bash
python svgViewer.py
```

# TODO
- jsonのデータでmin maxも保存する ○
- setter getter使っていこう ○
- regmoji.pyに書き直し ○
- jsonを正しく出力 書き出し中に例外が起こると出力がバグる
- resize関係についてリサイズできないようにするか対応させるか
- 入力データのフォーマット
- 正規化
- cancelやnextは入れるけどそれ以外にskipとか文字選択を作るか
- uiの装飾
- 統合するか
- 出力形式をどうするか(svgでいいらしい)
- A4 297mm, 210mm, (297000,210000)points
- linuxでpythonエディタを用意する ○ nvimとcocで良し
- validationをしておく，出力のチェックも
- 誤差を加える(オリジナリティ)
- マスに十字線 △ 部分的にそう
- ワープロに罫線
- 実際のデータを使ったフーリエテスト
- jsonの改行 ○ めんどくさい
- 複数ページ
- svgViewer

# 問題点
- cssが適用されない
- canvasのclear関数でcanvasが初期化されない
- フーリエ級数展開がうまく言ってるのかわからない
