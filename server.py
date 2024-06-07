import argparse
parser = argparse.ArgumentParser(description='TensorFlowのMultiProcessingモジュールを活用した分散学習のための情報交換サーバーを起動します。')
parser.add_argument("--host",type=str,help="Hostを指定します。",default="0.0.0.0")
parser.add_argument("-p","--port",type=int,help="Portを指定します。",default=2459)
import websockets
from logging import getLogger, config
import json
import asyncio

#実行時の引数を取得
args=parser.parse_args()
host=args.host
port=args.port

#ログの設定
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)

async def server(websocket, path):
    while True:
        # クライアントからデータを受け取る
        data = await websocket.recv()
        logger.info(f"Received data: {data}")

        # クライアントにデータを送信する
        await websocket.send("Data received")
def main():
    start_server = websockets.serve(server, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
if __name__ == "__main__":
    main()