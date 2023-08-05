# DStokuronn

# .md とはマークダウン コード　 CSV 実行結果

# state_wise_daily.csv 　　インドの各州のコロナの状態を表している。

# インドの各州のコロナの状態をグラフを用いて解析しました。

# 実行結果

![India_state_wise_daily](/image/India.png)

<!--
import pandas as pd
import numpy as np     配列の演算や分析作業
import sys                  Pythonのインタプリタや実行環境に関する情報を扱うためのライブラリ
from time import sleep      処理を一時的に停止する timeモジュールの中のsleepメソッドを使いたいのでインポートする
import matplotlib.pyplot as plt グラフ描画の標準的なライブラリ
import subprocess as sp     Python のプログラムから他のアプリを起動したり、実行結果を得たりするモジュール
from sklearn.metrics import r2_score as r2
import matplotlib.patches as mpatches


sp.call("wget https://data.covid19india.org/csv/latest/state_wise_daily.csv",shell=True) csvファイルを呼び出す
sp.call("cat state_wise_daily.csv|sed '2,$s/,-/,/g' >new",shell=True)  ファイルの内容を表示
sp.call("mv new state_wise_daily.csv",shell=True)  ファイルを移動
data=pd.read_csv("state_wise_daily.csv")
data.fillna(0,inplace=True) パラメータの追加
sp.call("rm state_wise_daily.csv",shell=True)



# print(data)
# plt.savefig("India_state_wise_daily.png")
print(data.plot())
print(plt.show())プロットしたグラフを描画
-->
