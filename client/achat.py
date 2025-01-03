import asyncio
import aioconsole
import sys
from aiohttp import ClientSession

from internal.commands import execute
from internal.state import State

async def main():
    if len(sys.argv) < 2:
        print("You must specify server address")
        sys.exit(1)
    state = State(server_url=sys.argv[1], session=ClientSession())
    command: str = await aioconsole.ainput("> ")
    while command != "exit":
        await execute(command.split(), state)
        command = await aioconsole.ainput("> ")

    await execute(['disconnect'], state)
    await state.session.close()

if __name__ == '__main__':
    asyncio.run(main())