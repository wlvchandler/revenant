import asyncio
import os
import signal
import sys
from typing import List

class Service:
    def __init__(self, name: str, script: str):
        self.name = name
        self.script = script
        self.process: asyncio.subprocess.Process = None

    async def start(self):
        python_cmd = sys.executable
        self.process = await asyncio.create_subprocess_exec(
            python_cmd, self.script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()

    async def read_output(self):
        while self.process:
            try:
                line = await asyncio.wait_for(self.process.stdout.readline(), timeout=0.1)
                if line:
                    print(f"[{self.name}] {line.decode().strip()}")
                elif self.process.returncode is not None:
                    break
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error reading output from {self.name}: {e}")
                break

async def run_services(services: List[Service]):
    await asyncio.gather(*(service.start() for service in services))
    await asyncio.gather(*(service.read_output() for service in services))

async def main():
    os.chdir("/home/will/testcode/revenant/modules")

    services = [
        Service("Generator", "msg_gen.py"),
        Service("Enricher", "msg_enrich.py"),
        Service("Processor", "msg_proc.py"),
        Service("Aggregator", "msg_agg.py")
    ]

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler():
        print("\nStopping all services...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        runner_task = asyncio.create_task(run_services(services))
        await stop_event.wait()
    finally:
        runner_task.cancel()
        await asyncio.gather(*(service.stop() for service in services))
        print("All services stopped.")

if __name__ == "__main__":
    asyncio.run(main())
