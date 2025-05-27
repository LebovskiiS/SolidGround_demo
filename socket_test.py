import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/chat/test/"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket!")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_websocket())