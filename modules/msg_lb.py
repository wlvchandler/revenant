import asyncio
import websockets
import json

class LoadBalancer:
    def __init__(self):
        self.processors = []
        self.current = 0

    def add_processor(self, processor):
        self.processors.append(processor)

    def get_next_processor(self):
        if not self.processors:
            return None
        processor = self.processors[self.current]
        self.current = (self.current + 1) % len(self.processors)
        return processor

async def balance_load():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:load_balancer")
        print("Registered as load_balancer")

        balancer = LoadBalancer()
        balancer.add_processor("processor1")
        balancer.add_processor("processor2")

        while True:
            message = await websocket.recv()
            _, payload = message.split(":", 1)
            data = json.loads(payload)
            
            next_processor = balancer.get_next_processor()
            if next_processor:
                await websocket.send(f"{next_processor}:{json.dumps(data)}")
                print(f"Routed message to {next_processor}: {data}")
            else:
                print("No processors available")

asyncio.get_event_loop().run_until_complete(balance_load())
