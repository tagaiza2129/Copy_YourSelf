import asyncio
import websockets

async def connect_to_websocket_server():
    async with websockets.connect('ws://localhost:2459') as websocket:
        # Perform actions with the WebSocket connection
        await websocket.send('connect Main_PC_For_tagaiza CPU GPU 8GB')
        while True:  # Keep the connection open
            try:
                response = await websocket.recv()
                print(f'Received message from server: {response}')
            except websockets.exceptions.ConnectionClosed:
                print("Connection with server closed")
                break

# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_to_websocket_server())