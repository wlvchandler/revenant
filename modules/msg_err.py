import asyncio
import websockets
import json

async def handle_errors():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:error_handler")
        print("Registered as error_handler")

        while True:
            raw_message = await websocket.recv()
            print(f"Received raw message: {raw_message}")
            
            try:
                data = json.loads(raw_message)
                
                if "error" in data:
                    print(f"Handling error: {data['error']}")
                    # Simulate error handling
                    await asyncio.sleep(0.01)
                    
                    resolution = {
                        "original_id": data["id"],
                        "error": data["error"],
                        "resolution": "Error handled and logged"
                    }
                    
                    await websocket.send(f"aggregator:{json.dumps(resolution)}")
                    print(f"Error handled: {resolution}")
                else:
                    print(f"Received non-error message: {data}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Problematic message: {raw_message}")
            except Exception as e:
                print(f"Error processing message: {e}")

asyncio.get_event_loop().run_until_complete(handle_errors())
