# Code adapted from webSocket quick starter guide:
# https://websockets.readthedocs.io/en/stable/intro/examples.html

import asyncio
import json
from websockets.asyncio.server import serve
from generator import get_registers, generate_notes

REGISTERS = get_registers() # once per run: PIECE_SPEC 6.3

async def handler(websocket):
    print("client connected")
    chord = generate_notes({"Red": 12, "Blue": 6, "Violet": 2}, REGISTERS) # any test vote dictionary
    text = "Hello from the server"
    message = {"type": "score", "page": 1, "text": text, "chord": chord}
    await websocket.send(json.dumps(message))
    async for raw in websocket:
        print("received:", raw)

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
