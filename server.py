import argparse
parser = argparse.ArgumentParser(description='TensorFlowのMultiProcessingモジュールを活用した分散学習のための情報交換サーバーを起動します。')
parser.add_argument("--host",type=str,help="Hostを指定します。",default="0.0.0.0")
parser.add_argument("-p","--port",type=int,help="Portを指定します。",default=2459)
import websockets
from logging import getLogger, config
import json
import asyncio
import json
#実行時の引数を取得
args=parser.parse_args()
argparse_host=args.host
argparse_port=args.port

#ログの設定
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)
Connection_List=[]
async def server(websocket, path):
    while True:
        # クライアントからデータを受け取る
        data = await websocket.recv()
        connection_command=data.split()
        #match分でJSのswitch文のように条件分岐
        match connection_command[0]:
            case "connect":
                Connection_List.append({"id":len(Connection_List),"address":websocket.remote_address,"name":connection_command[1],"cpu":connection_command[2],"gpu":connection_command[3],"memory":connection_command[4]})
                logger.info(f"Connected from IP:{websocket.remote_address} Name:{connection_command[1]}")
            case "connect_list":
                logger.info(f"Connected list")
            case "disconnect":
                logger.info(f"Disconnected from {websocket.remote_address}")
            case "Learning_Start":
                logger.info(f"Learning Start")
            case _:
                logger.info(f"Unknown Command {connection_command[0]}")
                await websocket.send("Unknown Command")
        # クライアントにデータを送信する
        await websocket.send("Data received")

def main(host, port):
    logger.info(f"WebSocketサーバーを起動しました {host}:{port}")
    start_server = websockets.serve(server, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main(argparse_host, argparse_port)