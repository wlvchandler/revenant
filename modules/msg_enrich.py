import asyncio
import websockets
import json
import random

async def enrich_data():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:enricher")
        print("Registered as enricher")

        while True:
            raw_message = await websocket.recv()
            print(f"Received raw message: {raw_message}")
            
            try:
                data = json.loads(raw_message)
                
                # Simulate data enrichment
                enriched_data = data.copy()
                enriched_data["timestamp"] = asyncio.get_event_loop().time()
                enriched_data["enriched_value"] = random.random()
                
                await asyncio.sleep(0.002)  # Simulated enrichment time
                
                await websocket.send(f"processor:{json.dumps(enriched_data)}")
                print(f"Enriched and sent: {enriched_data}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Problematic message: {raw_message}")
            except Exception as e:
                print(f"Error processing message: {e}")

asyncio.get_event_loop().run_until_complete(enrich_data())
