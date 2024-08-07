import asyncio
import websockets
import json
import random
import time
from collections import deque

async def generate_messages():
    uri = "ws://localhost:8080/ws"
    print("Message generator starting...")

    while True:
        try:
            print("Attempting to connect to the router...")
            async with websockets.connect(uri) as websocket:
                print("Connected to the router. Registering as generator...")
                await websocket.send("register:generator")
                print("Registered as generator. Starting message generation...")

                total_count = 0
                start_time = time.time()
                recent_messages = deque(maxlen=2000)  # Store timestamps of recent messages

                while True:
                    message = {
                        "id": random.randint(1, 1000000),
                        "content": f"Message {random.randint(1, 1000)}"
                    }
                    await websocket.send(f"enricher:{json.dumps(message)}")
                    
                    current_time = time.time()
                    total_count += 1
                    recent_messages.append(current_time)

                    if total_count % 1000 == 0: 
                        elapsed = current_time - start_time
                        recent_count = sum(1 for t in recent_messages if current_time - t <= 2)
                        
                        print(f"Messages:{total_count}\tTime:{elapsed:.2f}s\tRate:{total_count/elapsed:.2f} msg/s\tGen (2s):{recent_count}\tRate (2s):{recent_count/2:.2f} msg/s")

                    await asyncio.sleep(0.00001)
        except websockets.exceptions.ConnectionClosed:
            print("Connection to the router was closed. Attempting to reconnect...")
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Waiting 5 seconds before trying to reconnect...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    print("Script started. Entering main event loop...")
    asyncio.get_event_loop().run_until_complete(generate_messages())
    print("Script finished.")
