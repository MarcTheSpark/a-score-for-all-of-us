# Code adapted from webSocket quick starter guide:
# https://websockets.readthedocs.io/en/stable/intro/examples.html

import asyncio
import json
from websockets.asyncio.server import serve, broadcast
from generator import get_registers, generate_notes, COLOR
from pathlib import Path
import os

PORT = int(os.environ.get("PORT", 8765)) # use Render's PORT if set, otherwise port 8765
CONSOLE_KEY = os.environ.get("CONSOLE_KEY")

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

audience_clients = set()    # every joined audience phone
piece_started = False

# Voting state
vote_page = 0 # page audience is voting for
voting_open = False
choices = {} # phone connection->color chosen, color stops getting overwritten when time's up
vote_timer = None

# ============================================
def countdown_seconds(text):
    """10 s for 50 characters or fewer, 15 s for 100 or more, scaled evenly between (PIECE_SPEC 5)"""
    n = len(text)
    if n <= 50:
        return 10
    if n >= 100:
        return 15
    return 10 + (n - 50) / 50 * 5

def tally():
    """Count the current choices as {color: votes}"""
    counts = {color: 0 for color in COLOR}
    for color in choices.values():
        counts[color] += 1
    return counts

def send_vote_status():
    """Tell every console where the vote stands"""
    status = {"type": "voting", "page": vote_page, "open": voting_open,
              "voted": len(choices), "counts": tally()}
    broadcast(console_clients, json.dumps(status))
    
def open_vote(n):
    """Open the vote for page n on every phone, and schedule its end"""
    global vote_page, voting_open, choices, vote_timer
    if vote_timer is not None:
        vote_timer.cancel()                       # a jump replaces any running vote
    if not (1 <= n <= len(TEXT_LINES)):           # no line left to vote on
        voting_open = False
        vote_page = 0
        broadcast(audience_clients, json.dumps({"type": "vote_closed"}))
        send_vote_status()
        return
    vote_page = n
    voting_open = True
    choices = {}
    seconds = countdown_seconds(TEXT_LINES[n - 1])
    broadcast(audience_clients, json.dumps({"type": "vote_open", "page": n,
              "text": TEXT_LINES[n - 1], "seconds": seconds}))
    vote_timer = asyncio.get_running_loop().call_later(seconds, close_vote)
    send_vote_status()
    
def close_vote():
    """Called automatically when the countdown ends"""
    global voting_open
    voting_open = False
    broadcast(audience_clients, json.dumps({"type": "vote_closed"}))
    send_vote_status()
    
# ==========================================================

def send_room_status():
    """Tell console how many audience members joined and whether the piece started"""
    status = {"type": "room", "joined": len(audience_clients), "started": piece_started}
    broadcast(console_clients, json.dumps(status))

def build_page(n, counts):
    """Build the score message for page n (0 = empty staff)"""
    if n == 0:
        return {"type": "score", "page": 0, "text": "", "chord": []}
    chord = generate_notes(counts, REGISTERS)
    return {"type": "score", "page": n, "text": TEXT_LINES[n - 1], "chord": chord}

async def handler(websocket):
    global current_score, page_number, piece_started
    hello = json.loads(await websocket.recv())
#     print("hello received:", hello, "| server key:", CONSOLE_KEY)
    role = hello["role"]
    if role == "score":
        score_clients.add(websocket)
        await websocket.send(json.dumps(current_score))
        
    elif role == "console":
        if CONSOLE_KEY is None or hello.get("key") != CONSOLE_KEY:
            print("console rejected: wrong or missing key")
            await websocket.close()
            return       
        console_clients.add(websocket)
        await websocket.send(json.dumps(current_score))
        send_room_status()
        send_vote_status()
        
    elif role == "audience":
        if piece_started:
            await websocket.send(json.dumps({"type": "locked"}))
            await websocket.close()
            return
        audience_clients.add(websocket)
        send_room_status()
        
    try:
        async for raw in websocket:
            data = json.loads(raw)
            if role == "console" and data["type"] == "next_page":
                if page_number == len(TEXT_LINES):
                    print("Last line of text_score reached, X is ignored.")
                    continue
                
                if voting_open:
                    print("Voting still open, X is ignored.")
                    continue
                
                page_number += 1
                counts = data["counts"] if data.get("override") else tally()
                current_score = build_page(page_number, counts)
                broadcast(score_clients | console_clients, json.dumps(current_score))
                open_vote(page_number + 1)
                
            elif role == "console" and data["type"] == "go_to_page":
                target_page = data["page"]
                if not (0 <= target_page <= len(TEXT_LINES)):
                    print("go_to_page out of range:", target_page)
                    continue
                page_number = target_page
                current_score = build_page(page_number, data["counts"])
                broadcast(score_clients | console_clients, json.dumps(current_score))
                
                if piece_started:
                    open_vote(page_number + 1)
            
            elif role == "console" and data["type"] == "start_piece":
                piece_started = True
                send_room_status()
                open_vote(1)
                
            # for the phone's votes    
            elif role == "audience" and data["type"] == "vote":
                if voting_open and data.get("color") in COLOR:
                    choices[websocket] = data["color"]
                    send_vote_status()
            
    finally:
        score_clients.discard(websocket)
        console_clients.discard(websocket)
        audience_clients.discard(websocket)
        send_room_status()
        

async def main():
    async with serve(handler, "0.0.0.0", PORT) as server: # listen on every network connection this machine has 
        await server.serve_forever()

asyncio.run(main())
