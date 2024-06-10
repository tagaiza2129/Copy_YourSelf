import argparse
parser = argparse.ArgumentParser(description='TensorFlowのMultiProcessingモジュールを活用した分散学習のための情報交換サーバーを起動します。')
parser.add_argument("--host",type=str,help="Hostを指定します。",default="0.0.0.0")
parser.add_argument("-p","--port",type=int,help="Portを指定します。",default=2459)
import websockets
from logging import getLogger, config
import json
import asyncio
import json
import signal
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
        try:
        # クライアントからデータを受け取る
            data = await websocket.recv()
            connection_command=data.split()
            #match分でJSのswitch文のように条件分岐
            match connection_command[0]:
                case "connect":
                    Connection_List.append({"id":len(Connection_List),"address":websocket.remote_address[0],"name":connection_command[1],"cpu":connection_command[2],"gpu":connection_command[3],"memory":connection_command[4]})
                    logger.info(f"Connected from IP:{websocket.remote_address[0]} Name:{connection_command[1]}")
                    await websocket.send(f"Connected {len(Connection_List)}")
                case "connect_list":
                    logger.info(f"Connected list")
                    await websocket.send(f"{json.dumps(Connection_List)}")
                case "disconnect":
                    await websocket.send(f"Disconnect {connection_command[1]}")
                    Connection_List[:] = [d for d in Connection_List if d.get('address') != websocket.remote_address]
                    logger.info(f"以下のIPアドレスの接続を切りました {websocket.remote_address}")
                case "Learning_Start":
                    logger.info(f"Learning Start")
                case _:
                    logger.info(f"知らないコマンドです...コードを参照してください\nError: {connection_command[0]}")
                    await websocket.send("Unknown Command")
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection Closed from {websocket.remote_address}")
            Connection_List[:] = [d for d in Connection_List if d.get('address') != websocket.remote_address]
            break
        except KeyboardInterrupt:
            logger.info(f"WebSocket サーバーが停止しました")
            break

def main(host, port):
    logger.info(f"WebSocketサーバーを起動しました {host}:{port}")
    loop = asyncio.get_event_loop()

    # Set up the signal handler
    loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())

    # Start the server
    start_server = websockets.serve(server, host, port)  # Use the 'server' function defined outside of 'main'
    server_task = loop.run_until_complete(start_server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info(f"Server Closed")
    finally:
        # Cancel all tasks lingering
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        # Gather all tasks to give them the opportunity to cancel
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()
        logger.info(f"Server Closed")

if __name__ == "__main__":
    main(argparse_host, argparse_port)