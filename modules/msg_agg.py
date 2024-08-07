import asyncio
import websockets
import json
import time

async def aggregate_results():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:aggregator")
        print("Registered as aggregator")

        start_time = time.time()
        message_count = 0
        error_count = 0

        while True:
            raw_message = await websocket.recv()
            
            try:
                data = json.loads(raw_message)
                message_count += 1
                
                if "error" in data:
                    error_count += 1
                
                if message_count % 1000 == 0:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    throughput = message_count / elapsed_time
                    error_rate = error_count / message_count
                    print(f"Throughput: {throughput:.2f} messages/second, Error rate: {error_rate:.2%}")
                    
                    # Reset counters and start time for the next batch
                    start_time = current_time
                    message_count = 0
                    error_count = 0
                    
            except json.JSONDecodeError:
                print("Received invalid JSON")
            except Exception as e:
                print(f"Error processing message: {e}")

asyncio.get_event_loop().run_until_complete(aggregate_results())
