# Code adapted from webSocket quick starter guide:
# https://websockets.readthedocs.io/en/stable/intro/examples.html

import asyncio
import json
from websockets.asyncio.server import serve, broadcast
from generator import get_registers, generate_notes

REGISTERS = get_registers() # once per run: PIECE_SPEC 6.3
score_clients = set()       # every connected score page
current_score = {"type": "score", "page": 0, "text": "", "chord": []}   # page 0 = empty staff

async def handler(websocket):
    hello = json.loads(await websocket.recv()) # wait for the first message
    if hello["role"] == "score":
        score_clients.add(websocket)
        await websocket.send(json.dumps(current_score))  # late joiners get the current page
    try:
        async for raw in websocket:
            print("received:", raw)
    finally:
        score_clients.discard(websocket)       # remove it when it disconnects

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
