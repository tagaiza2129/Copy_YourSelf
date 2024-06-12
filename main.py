import argparse
#パラメーター(実行時の引数の設定)
#何で全てインポートした上でパラメーターの設定をしないのかって？TensorFlowのロードが始まると大量のログが流れて
#大変不格好だからだよ？
parser = argparse.ArgumentParser(prog="Copy_YourSelf",description='TensorFlow等を活用し、人格形成を学習させたChatBotを作成したいです...',usage="python3 main.py <file_Path> <options>",add_help=True)
parser.add_argument("processing_data",type=str,help="学習に利用するデータを指定します。")
parser.add_argument('-d', '--device',type=str,help='学習に利用するデバイスを指定します。\n使用想定デバイス\nCPU:まあ...そのままの意味\nGPU:NVIDIA製のGPUを利用し学習します\nXPU:intel製のGPUを利用し学習します',default="CPU")
parser.add_argument("-p","--port",type=int,help="分散学習に利用するサーバーのポートを指定します",default=2459)
parser.add_argument("-e","--epoch",type=int,help="何回繰り返し学習させるかを指定します。",default=10)
parser.add_argument("-s","--server_multi_processing",type=bool,help="分散学習を行うかどうかを指定します。",default=False)
parser.add_argument("-m","--mode",type=str,help="学習から推論までのモードを指定します。\n学習:学習を行います。\n推論:推論を行います。",default="学習")
args = parser.parse_args()
#指定された引数を受け取る、又、デフォルト値を設定しているため、引数が指定されなかった場合はデフォルト値が適用されるものとする
Processing_data=args.processing_data
device=args.device
port=args.port
epoch=args.epoch
multi_processing=args.server_multi_processing
mode=args.mode
import os
import time
import Preprocessing.analysis as analysis
from pathlib import Path
from logging import getLogger, config
import json
import subprocess
import tools
# ログの設定
with open('設定ファイル/log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)
os.chdir(os.path.dirname(__file__))
#Word2Vecのモデルが存在しない場合はダウンロードを行う
if os.path.isfile(os.path.join(os.path.dirname(__file__),"Preprocessing","word2vec.model")) ==False:
    logger.info("学習データのダウンロードを開始します...")
    tools.Drive_Download("Word2Vec","Preprocessing")
    logger.info("学習データのダウンロードが完了しました。")
#分散学習のためのサーバーを起動
if multi_processing==True:
    subprocess.Popen("python3 server.py",shell=True)
#MeCabの環境変数の設定
os.environ["MECABRC"]="/etc/mecabrc"
#送られてきた学習データが絶対パスか相対パスかを判定し、相対パスであれば絶対パスに変換している
#ちなみに自動変換を使った結果わけがわからんところに飛ばされたから実行ファイルを参照して無理やり変換している
if Path(Processing_data).is_absolute()==True:
    pass
else:
    Processing_data=os.path.join(os.path.dirname(__file__),Processing_data)
logger.info("ファイルの前準備を開始します...")
#上のログの通り、学習ファイルの前準備を行う、具体的には集めたデータのいらないデータを消去して対象ユーザー(金子拓夢)以外のテキストデータを削除している
#受け答えを学習させるために後々編集する予定...
os.chdir(Processing_data)
file_list=os.listdir(Processing_data)
Processing_data=[]
for file in file_list:
    os.chdir(Processing_data)
    with open(file,mode="r",encoding="UTF-8")as f:
        text_data=f.read()
    datas=text_data.split("\n")
    Analysis_mode=datas[0]
    for data in datas:
        text_data_list=data.split()
        if Analysis_mode=="LINE":
            if "[スタンプ]" in text_data_list or "[通話]" in text_data_list or "[画像]" in text_data_list or "http" in text_data_list or text_data_list[0]=="LINE":
                pass
            elif text_data_list[1]=="拓夢" or text_data_list[1]=="ターガイザー":
                Processing_data.append(text_data_list[2])
        elif Analysis_mode=="Discord":
            if len(text_data_list)<=1:
                pass
            elif "http" in text_data_list[1] or text_data_list==[] or "<@" in text_data_list[1] or "<#" in text_data_list[1] or "@here" in text_data_list[1] or "@everyone" in text_data_list[1] or "m!" in text_data_list[1]:
                pass
            elif text_data_list[0]=="tagaiza2129":
                try:
                    Processing_data.append(text_data_list[1])
                except IndexError:
                    pass
time.sleep(0.5)
logger.info("形態素解析中...")
Morphological_data=analysis.Morphological_analysis(Processing_data)
logger.info("ベクトル化処理中...")
vector_data=analysis.vector(Morphological_data)
print(vector_data)