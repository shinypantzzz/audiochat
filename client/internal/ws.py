import aiohttp
import asyncio
from datetime import datetime

from .audioio import AudioIO
from .storage import Storage

class Connection:
    def __init__(self, room: str, url: str, io: AudioIO, storage: Storage, session: aiohttp.ClientSession):
        self.send_rate = io.latency
        self.io = io
        self.storage = storage
        self.url = url
        self.session = session
        self.room = room

    async def run(self):
        self.running = True
        self.ws = await self.session.ws_connect(self.url + "/connect", params={"room": self.room})
        if self.ws.exception():
            raise self.ws.exception()
        
        self.storage.add_server({
            'url': self.url,
            'rooms': [],
            'connection_datetime': datetime.now().isoformat()
        })
        self.io.start()
        async def send():
            while self.running:
                await self.ws.send_bytes(self.io.read())
                await asyncio.sleep(self.send_rate)
        asyncio.create_task(send())
        
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                self.io.write(msg.data)

    async def close(self):
        self.running = False
        await self.ws.close()
        self.io.stream.close()
        self.io.p.terminate()