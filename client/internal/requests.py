from aiohttp import client

class HttpException(Exception):
    pass

async def create_room(session: client.ClientSession, url: str, room_name: str):
    async with session.post(url + '/create_room', data={"name": room_name}) as response:
        if response.status != 200:
            raise HttpException((await response.text()).strip())