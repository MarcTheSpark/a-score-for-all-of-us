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
TEXT_LINES = [line for line in raw_lines if line.strip()]   # skip blank lines

REGISTERS = get_registers() # once per run: PIECE_SPEC 6.3
score_clients = set()       # every connected score page
console_clients = set()     # every connected console page
current_score = {"type": "score", "page": 0, "text": "", "chord": []}   # page 0 = empty staff
page_number = 0

def build_page(n, counts):
    """Build the score message for page n (0 = empty staff)"""
    if n == 0:
        return {"type": "score", "page": 0, "text": "", "chord": []}
    chord = generate_notes(counts, REGISTERS)
    return {"type": "score", "page": n, "text": TEXT_LINES[n - 1], "chord": chord}

async def handler(websocket):
    global current_score, page_number
    hello = json.loads(await websocket.recv())
    role = hello["role"]
    if role == "score":
        score_clients.add(websocket)
        await websocket.send(json.dumps(current_score))
    elif role == "console":
        console_clients.add(websocket)
        await websocket.send(json.dumps(current_score))
    try:
        async for raw in websocket:
            data = json.loads(raw)
            if role == "console" and data["type"] == "next_page":
                if page_number == len(TEXT_LINES):
                    print("Last line of text_score reached, X is ignored.")
                    continue        
                page_number += 1
                current_score = build_page(page_number, data["counts"])
                broadcast(score_clients | console_clients, json.dumps(current_score))
                
            elif role == "console" and data["type"] == "go_to_page":
                target_page = data["page"]
                if not (0 <= target_page <= len(TEXT_LINES)):
                    print("go_to_page out of range:", target_page)
                    continue
                page_number = target_page
                current_score = build_page(page_number, data["counts"])
                broadcast(score_clients | console_clients, json.dumps(current_score))
            
    finally:
        score_clients.discard(websocket)
        console_clients.discard(websocket)
        

async def main():
    async with serve(handler, "0.0.0.0", PORT) as server: # listen on every network connection this machine has 
        await server.serve_forever()

asyncio.run(main())
