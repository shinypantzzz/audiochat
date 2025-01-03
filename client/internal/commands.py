from typing import Callable
from pathlib import Path
import asyncio

from .storage import Storage
from .ws import Connection
from .audioio import AudioIO
from .state import State
from .requests import create_room, HttpException

commands = {}
async def execute(args: list[str], state: State):
    if args[0] in commands:
        await commands[args[0]](args[1:], state)
    else:
        print("Unknown command:", args[0])

def command(f: Callable):
    commands[f.__name__] = f
    return f

@command
async def create(args: list[str], state: State):
    usage = "create [name]"
    if len(args) < 1:
        print(f"Usage: {usage}")
        return
    name = args[0]
    try:
        await create_room(state.session, state.server_url, name)
    except HttpException as e:
        print(f"Failed to create room: {e}")
        return
    
    print(f"Created room: {name}.")
    await connect([name], state)

@command
async def connect(args: list[str], state: State):
    usage = "connect [room_name]"
    if len(args) >= 1:
        room = args[0]
    elif stored_room := state.storage.get_most_recent_room(state.server_url):
        room = stored_room
    else:
        print(f"Usage: {usage}")
        return

    if state.conn:
        await state.conn.close()
    
    print(f"Connecting...")

    io = AudioIO()
    state.conn = Connection(room, state.server_url, io, state.storage, state.session)

    asyncio.create_task(state.conn.run())

@command
async def disconnect(args: list[str], state: State):
    if state.conn:
        await state.conn.close()

@command
async def vol(args: list[str], state: State):
    usage = "vol [volume]"
    if len(args) < 1:
        print(f"Usage: {usage}")
        return
    if state.conn:
        volume = float(args[0]) if len(args) >= 1 else 1.0
        state.conn.io.volume = volume