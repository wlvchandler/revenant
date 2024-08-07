import asyncio
import websockets
import json
import random
import time

async def process_messages():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:processor")
        print("Registered as processor")

        count = 0
        start_time = time.time()
        while True:
            raw_message = await websocket.recv()
            
            try:
                data = json.loads(raw_message)
                if random.random() < 0.05:  # 5% chance of error
                    error_msg = {"id": data["id"], "error": "Simulated processing error"}
                    await websocket.send(f"error_handler:{json.dumps(error_msg)}")
                else:
                    result = {
                        "id": data["id"],
                        "result": f"Processed {data['content']}",
                        "enriched_value": data.get("enriched_value", "N/A"),
                        "processing_time": asyncio.get_event_loop().time() - data.get("timestamp", 0)
                    }
                    await websocket.send(f"aggregator:{json.dumps(result)}")
                count += 1
                if count % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(f"Processor: Processed {count} messages in {elapsed:.2f} seconds. Rate: {count/elapsed:.2f} messages/second")
                    count = 0
                    start_time = time.time()
            except Exception as e:
                print(f"Processor error: {e}")

asyncio.get_event_loop().run_until_complete(process_messages())
