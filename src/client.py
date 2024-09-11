#複数PCで分散学習を行う際のクライアントコード
import argparse
parser = argparse.ArgumentParser(prog="Copy_YourSelf-Client",description='AIツール、CopyYourSelfのクライアント側のツール',usage="python3 main.py <file_Path> <options>",add_help=True)
parser.add_argument("server_address",type=str,help="学習、又は推論に利用するデータを指定します。")
parser.add_argument('-d', '--device',type=str,help='学習に利用するデバイスを指定します。\n使用想定デバイス\nCPU:まあ...そのままの意味\nGPU:NVIDIA製のGPUを利用し学習します\nXPU:intel製のGPUを利用し学習します',default="CPU")
parser.add_argument("-p","--port",type=int,help="分散学習に利用するサーバーのポートを指定します",default=2459)
args = parser.parse_args()
s_address=args.server_address
device=args.device
port=args.port
#引数の処理を先に行う理由はインポート時にログを残すモジュールがありヘルプコマンドのじゃまになるため
import websockets
#...今気づいたけど分散学習のファイル共有の為にWebSocket使うんだったらサーバーサイドのRust側にも実装せなあかんやんけメンドイなぁ
import inference.RNN as RNN
