import asyncio
import websockets
import sys
args=sys.argv
async def connect_to_websocket_server():
    async with websockets.connect('ws://localhost:2459') as websocket:
        # Perform actions with the WebSocket connection
        await websocket.send(" ".join(args[1:]))
        responce = await websocket.recv()
        print(f'サーバーから帰ってきたデータ: {responce}')
        await websocket.close()

# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_to_websocket_server())