import websockets
import asyncio
import json
import time
import multiprocessing as mp
import requests
from utils import pretf



class Binance_wss:
    _ports = (443, 9443)

    def __init__(self, port_index: int = 0) -> None:
        if port_index < 0 or port_index >= len(self._ports):
            raise ValueError(f"Invalid port index, choose between 0 and {len(self._ports) - 1}")

    @property
    def url(self):
        return "wss://stream.binance.com:9443/ws/bnbbtc@depth"
        # f"wss://ws-api.binance.com:{self.port}/ws-api/v3/bnbbtc@depth@100ms"

    def next_port(self):
        next_index = (self._ports.index(self.port) + 1) % len(self._ports)
        self.port = self._ports[next_index]

    # Get data from the socket
    async def listen(self, url: str, queue: asyncio.Queue) -> None:
        async with websockets.connect(url) as websocket:
            while True:
                print("hi")
                wss_res = await websocket.recv()
                await queue.put(json.loads(wss_res))  # store data in queue

    # Tranfer data from the async queue to the process queue
    async def get_data(self, data_queue : asyncio.Queue, process_queue: mp.Queue, buffer_size: int = 1_000):
        buffer = []
        while True:
            print("hello")
            data = await data_queue.get()  # get data from asyncio.Queue
            buffer.append(data)
            if len(buffer) >= buffer_size:
                process_queue.put(buffer)  # put buffer in multiprocessing.Queue
                buffer = []

    def dump_data(self, process_queue: mp.Queue):
        while True:
            buffer = process_queue.get()
            if buffer is None:
                break
            try:
                with open(r'C:\Users\fazio\OneDrive\Documents\nap\wsoc\first_wws_output.json', 'r') as json_file:
                    existing_data = json.load(json_file)
                    existing_data.append(buffer)
            except FileNotFoundError:
                existing_data = []
                existing_data.append(buffer)
            finally: 
                with open(r'C:\Users\fazio\OneDrive\Documents\nap\wsoc\first_wws_output.json', 'w') as json_file:
                    json_file.write(json.dumps(existing_data))
                    #json.dump(existing_data, json_file)
                    print("uuu dumping")


async def main():
    wss_queue = asyncio.Queue(maxsize=6)  # adjust maxsize as needed
    process_queue = mp.Queue()
    
    a = Binance_wss()
    buffer_size = 6  # adjust as needed

    # spawn listen task
    listen_task = asyncio.create_task(a.listen(a.url, wss_queue))
    # spawn get_data task
    get_data_task = asyncio.create_task(a.get_data(data_queue= wss_queue, process_queue= process_queue, buffer_size= buffer_size))

    # start dump_data process
    process = mp.Process(target=a.dump_data, args=(process_queue,))
    process.start()

    await asyncio.gather(listen_task, get_data_task)

    # send None to indicate that there's no more data and the process should finish
    process_queue.put(None)
    process.join()  # wait for the process to finish

if __name__ == "__main__":
    asyncio.run(main())
