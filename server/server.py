# Code adapted from webSocket quick starter guide:
# https://websockets.readthedocs.io/en/stable/intro/examples.html

import asyncio
import json
from websockets.asyncio.server import serve, broadcast
from generator import get_registers, generate_notes
from pathlib import Path
import os

PORT = int(os.environ.get("PORT", 8765)) # use Render's PORT if set, otherwise port 8765

HERE = Path(__file__).parent # the folder this .py file lives in
TEXT_SCORE_FILE = HERE/"text_score.txt" # joins the paths

# Read the text score once at startup, one page per non-blank line
raw_lines = TEXT_SCORE_FILE.read_text(encoding="utf-8").splitlines()
TEXT_LINES = [line for line in raw_lines if line.strip()]   # skip blank lines and remove blanks from both ends

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
                if page_number == len(TEXT_LINES):
                    print("Last line of text_score reached, X is ignored.")
                    
                page_number += 1
                chord = generate_notes(data["counts"], REGISTERS)
                current_score = {"type": "score", "page": page_number,
                                 "text": TEXT_LINES[page_number - 1], "chord": chord}
                broadcast(score_clients, json.dumps(current_score))
    finally:
        score_clients.discard(websocket)
        

async def main():
    async with serve(handler, "0.0.0.0", 8765) as server: # listen on every network connection this machine has 
        await server.serve_forever()

asyncio.run(main())
