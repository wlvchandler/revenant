import asyncio
import websockets
import json
import time

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.message_count = 0
        self.error_count = 0

    def update(self, message):
        self.message_count += 1
        if "error" in message:
            self.error_count += 1

    def get_metrics(self):
        elapsed_time = time.time() - self.start_time
        return {
            "total_messages": self.message_count,
            "errors": self.error_count,
            "messages_per_second": self.message_count / elapsed_time,
            "error_rate": self.error_count / self.message_count if self.message_count > 0 else 0
        }

async def collect_metrics():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("register:metrics_collector")
        print("Registered as metrics_collector")

        collector = MetricsCollector()

        while True:
            message = await websocket.recv()
            _, payload = message.split(":", 1)
            data = json.loads(payload)
            
            collector.update(data)
            
            if collector.message_count % 1000 == 0:
                metrics = collector.get_metrics()
                print(f"Current metrics: {metrics}")

asyncio.get_event_loop().run_until_complete(collect_metrics())
