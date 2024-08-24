import unittest
import inference.RNN as RNN
import json
import requests
server_ip:str
port:int
#Pythonでの外部からのユニットテストを書きながらRNNやLSTMの実装を行う
#真面目に時間が無くなってきたからねしょうがないね
def lstm(date_json:dict):
    print(f"ユーザーデータ:{date_json}")

def get(server_ip:str,url_pass:str):
    response = requests.get(server_ip+url_pass)
    return response.text,response.status_code

def post(server_ip:str,url_pass:str,date_json:json):
    response = requests.post(server_ip+url_pass,date_json)
    return response.text,response.status_code

class TestTashizan(unittest.TestCase):
    def test_api(self):
        #GPUの確認APIのテスト
        test_1 = get(f"http://{server_ip}:{port}","/available_device")
        self.assertEqual(test_1[2],200)
        #学習APIのテスト
        test_json_1 = {"model_name":"学習させるAIの名前","Learning_File":"学習させるテキストデータ","Extensions":"拡張機能のID","mode":"test"}
        test_2=post(f"http://{server_ip}:{port}","/Learning",json.dump(test_json_1))
        self.assertEqual(test_2[2],200)
        #モデル作成APIのテスト
        test_json_2 = {"model_name":"学習させるAIの名前","Learning_File":"学習させるテキストデータ","Extensions":["拡張機能のID"],"mode":"test"}
        test_3=post(f"http://{server_ip}:{port}","/make_model",json.dump(test_json_2))
        self.assertEqual(test_3[2],200)
        #失敗時のテスト
        test_json_1.pop("model_name")
        test_4=post(f"http://{server_ip}:{port}","/Learning",json.dump(test_json_1))
        self.assertEqual(test_4[2],400)
        test_json_2.pop("model_name")
        test_5=post(f"http://{server_ip}:{port}","/make_model",json.dump(test_json_2))
        self.assertEqual(test_5[2],400)
        test_6=get(f"http://{server_ip}:{port}","/くぁｗせｄｒｆｔｇｙふじこｌｐ")
        self.assertEqual(test_6[2],404)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="Copy_YourSelf UnitTest",description='AIツール、CopyYourSelfのクライアント側のツール',usage="python3 main.py <file_Path> <options>",add_help=True)
    parser.add_argument("server_address",type=str,help="学習、又は推論に利用するデータを指定します。")
    parser.add_argument("-p","--port",type=int,help="分散学習に利用するサーバーのポートを指定します",default=2459)
    parser.add_argument("-m","--mode",type=str,help="テストのモードを指定します",choices=["test","unittest"],default="test")
    args = parser.parse_args()
    server_ip=args.server_address
    port=args.port
    if args.mode=="unittest":
        unittest.main()
    else:
        print("デバッグを開始します？\nえ？UnitTestもデバッグだって？\n...せやな")