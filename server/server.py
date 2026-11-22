# Code adapted from webSocket quick starter guide:
# https://websockets.readthedocs.io/en/stable/intro/examples.html

import asyncio
import json
from websockets.asyncio.server import serve, broadcast
from generator import get_registers, generate_notes

REGISTERS = get_registers() # once per run: PIECE_SPEC 6.3
score_clients = set()       # every connected score page
current_score = {"type": "score", "page": 0, "text": "", "chord": []}   # page 0 = empty staff
page_number = 0

async def handler(websocket):
    global current_score, page_number
    hello = json.loads(await websocket.recv())
    role = hello["role"]
    if role == "score":
        score_clients.add(websocket)
        await websocket.send(json.dumps(current_score))
    try:
        async for raw in websocket:
            data = json.loads(raw)
            if role == "console" and data["type"] == "next_page":
                page_number += 1
                chord = generate_notes(data["counts"], REGISTERS)
                current_score = {"type": "score", "page": page_number,
                                 "text": f"Page {page_number}", "chord": chord}
                broadcast(score_clients, json.dumps(current_score))
    finally:
        score_clients.discard(websocket)
        

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
