import asyncio
import json
import websockets

async def test():
    async with websockets.connect("ws://localhost:8000/ws/transactions/?user_id=1") as websocket:
        # Listen for messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received message: {data}")

asyncio.run(test())
