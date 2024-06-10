import asyncio
import websockets
connect_info={}
async def connect_to_websocket_server():
    async with websockets.connect('ws://localhost:2459') as websocket:
        # Perform actions with the WebSocket connection
        await websocket.send('connect Main_PC_For_tagaiza CPU GPU 8GB')
        while True:  # Keep the connection open
            try:
                response = await websocket.recv()
                response_order=response.split()
                match response_order[0]:
                    case "Connected":
                        connect_info["id"]=response_order[1]
                    case "Connected_list":
                        print(response_order[1])
                    case "Disconnect":
                        if response_order[1]==connect_info["id"]:
                            print("サーバーから切断されました")
                            break
                    case "Unknown":
                        print("Unknown Command")
            except websockets.exceptions.ConnectionClosed:
                print("Connection with server closed")
                break

# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_to_websocket_server())