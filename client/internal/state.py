from pathlib import Path
from dataclasses import dataclass

from aiohttp import ClientSession

from .ws import Connection
from .storage import Storage

@dataclass
class State:
    server_url: str
    session: ClientSession
    conn: Connection | None = None
    storage: Storage = Storage(Path(__file__).parent / "db.json")