import argparse
#パラメーター(実行時の引数の設定)
#何で全てインポートした上でパラメーターの設定をしないのかって？TensorFlowのロードが始まると大量のログが流れて
#大変不格好だからだよ？
parser = argparse.ArgumentParser(prog="Copy_YourSelf",description='TensorFlow等を活用し、人格形成を学習させたChatBotを作成したいです...',usage="python3 main.py <file_Path> <options>",add_help=True)
parser.add_argument("processing_data",type=str,help="学習、又は推論に利用するデータを指定します。")
parser.add_argument('-d', '--device',type=str,help='学習に利用するデバイスを指定します。\n使用想定デバイス\nCPU:まあ...そのままの意味\nGPU:NVIDIA製のGPUを利用し学習します\nXPU:intel製のGPUを利用し学習します',default="CPU")
parser.add_argument("-p","--port",type=int,help="分散学習に利用するサーバーのポートを指定します",default=2459)
parser.add_argument("-e","--epoch",type=int,help="何回繰り返し学習させるかを指定します。",default=10)
parser.add_argument("-s","--server_multi_processing",type=bool,help="分散学習を行うかどうかを指定します。",default=False)
parser.add_argument("-m","--mode",type=str,help="学習から推論までのモードを指定します。\n学習:学習を行います。\n推論:推論を行います。",default="学習")
parser.add_argument("-l","--Lerning_mode",type=str,choices=["Word2Vec","RNN"],help="学習モデルを指定します。\nWord2Vec:Word2Vecを学習します。\nRNN:RNNを学習します。",default="RNN")
args = parser.parse_args()
#指定された引数を受け取る、又、デフォルト値を設定しているため、引数が指定されなかった場合はデフォルト値が適用されるものとする
Processing_data=args.processing_data
device=args.device
port=args.port
epoch=args.epoch
multi_processing=args.server_multi_processing
mode=args.mode
Lerning_mode=args.Lerning_mode
import os
import time
import Preprocessing.analysis as analysis
from pathlib import Path
from logging import getLogger, config
import json
import subprocess
import tools
import Preprocessing.Word2Vec_Learning as Word2Vec
#学習モードがWord2Vecの場合はWord2Vecの学習を行い終了する
if Lerning_mode=="Word2Vec":
    Word2Vec.Lerning(Processing_data,epoch)
    exit()
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
os.chdir(os.path.dirname(__file__))
logger.info("ファイルの前準備を開始します...")
#上のログの通り、学習ファイルの前準備を行う、具体的には集めたデータのいらないデータを消去して対象ユーザー(金子拓夢)以外のテキストデータを削除している
#受け答えを学習させるために後々編集する予定...
os.chdir(Processing_data)
file_list=os.listdir(Processing_data)
Processing_data=[]
for file in file_list:
    with open(file,mode="r",encoding="UTF-8")as f:
        text_data=f.read()
    Processing_data=text_data.split("\n")
time.sleep(0.5)
logger.info("形態素解析中...")
Morphological_data=analysis.Morphological_analysis(Processing_data)
logger.info("ベクトル化処理中...")
vector_data=analysis.vector(Morphological_data)
print(vector_data)