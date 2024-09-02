import unittest
import json
import yaml
import requests
import os
os.chdir(os.path.dirname(__file__))
os.chdir("../")
app_dir=os.getcwd()
with open("config.yaml") as f:
    config = yaml.safe_load(f)
    server_ip = str(config["server_ip"])
    port = int(config["server_port"])
#Pythonでの外部からのユニットテストを書きながらRNNやLSTMの実装を行う
#真面目に時間が無くなってきたからねしょうがないね
def lstm(date_json:dict):
    print(f"ユーザーデータ:{date_json}")

def get(server_ip:str,url_pass:str):
    response = requests.get(server_ip+url_pass)
    return [response.text,response.status_code]

def post(server_ip:str,url_pass:str,date_json:json):
    response = requests.post(server_ip+url_pass,date_json)
    return [response.text,response.status_code]

class TestTashizan(unittest.TestCase):
    def test_api(self):
        #GPUの確認APIのテスト
        test_1 = get(f"http://{server_ip}:{port}","/available_device")
        self.assertEqual(test_1[1],200)
        #学習APIのテスト
        test_json_1 = {"model_name":"学習させるAIの名前","Learning_File":"学習させるテキストデータ","Extensions":"拡張機能のID","mode":"test"}
        test_2=post(f"http://{server_ip}:{port}","/Learning",json.dumps(test_json_1))
        self.assertEqual(test_2[1],200)
        #モデル作成APIのテスト
        test_json_2 = {"model_name":"学習させるAIの名前","Learning_File":"学習させるテキストデータ","Extensions":["拡張機能のID"],"mode":"test"}
        test_3=post(f"http://{server_ip}:{port}","/make_model",json.dumps(test_json_2))
        self.assertEqual(test_3[1],200)
        #失敗時のテスト
        test_json_1.pop("model_name")
        test_4=post(f"http://{server_ip}:{port}","/Learning",json.dumps(test_json_1))
        self.assertEqual(test_4[1],400)
        test_json_2.pop("model_name")
        test_5=post(f"http://{server_ip}:{port}","/make_model",json.dumps(test_json_2))
        self.assertEqual(test_5[1],400)
        test_6=get(f"http://{server_ip}:{port}","/くぁｗせｄｒｆｔｇｙふじこｌｐ")
        self.assertEqual(test_6[1],404)

