import asyncio
import websockets

async def test_admin_websocket():
    uri = "ws://127.0.0.1:8000/ws/admin/"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Admin WebSocket!")
            # Wait for a moment to see if the connection stays open
            await asyncio.sleep(2)
            print("Connection remained open for 2 seconds, test passed!")
    except Exception as e:
        print(f"Error: {e}")
        print("Test failed - could not connect to admin WebSocket endpoint")

if __name__ == "__main__":
    print("Testing connection to admin WebSocket endpoint...")
    asyncio.run(test_admin_websocket())