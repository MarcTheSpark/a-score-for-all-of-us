import random

# CONSTANTS
COLOR = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
DORIAN_SCALE = ["D", "E", "F", "G", "A", "B", "C"]
COLOR_INTERVAL_MAP = {
        "Red": (DORIAN_SCALE[0], DORIAN_SCALE[1]),
        "Orange": (DORIAN_SCALE[1], DORIAN_SCALE[2]),
        "Yellow": (DORIAN_SCALE[2], DORIAN_SCALE[3]),
        "Green": (DORIAN_SCALE[3], DORIAN_SCALE[4]),
        "Blue": (DORIAN_SCALE[4], DORIAN_SCALE[5]),
        "Indigo": (DORIAN_SCALE[5], DORIAN_SCALE[6]),
        "Violet": (DORIAN_SCALE[6], DORIAN_SCALE[0])
        }

NOTES = {
        'C': 0, 'C#': 1, 'Db': 1,
        'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
        'G': 7, 'G#': 8, 'Ab': 8,
        'A': 9, 'A#': 10, 'Bb': 10,
        'B': 11
        }

INCLUDE_PCENT_LINE = 0.15 # Any color (interval) above 15% gets included. (Rule 6.2)
MAJORITY_PCENT_LINE = 0.5 # Color rules 6.2.3
LOWEST_NOTE = 48 # C3
HIGHEST_NOTE = 84 # C6

def get_midi_num(pitch: str, octave: int):
    return 12 * (octave + 1) + NOTES[pitch]

def get_registers():
    """Picks an octave for each pitch and store it"""
    registers = {}
    for pitch in DORIAN_SCALE:
        allowed_octaves = []
        for octave in range(3, 7):
            if LOWEST_NOTE <= get_midi_num(pitch, octave) and HIGHEST_NOTE >= get_midi_num(pitch,octave):
                allowed_octaves.append(octave)
        registers[pitch] = random.choice(allowed_octaves) # picks an octave for the pitch and store it
    return registers
        
# print(get_registers())

def votes_to_shares(votes_count: dict[str, int]):
    """Convert Audience Votes to Shares"""
    total = sum(votes_count.values())
    if total == 0:
        return None
    shares = {}
    for color, count in votes_count.items():
        shares[color] = count / total
    return shares

def choose_pitches(shares):
    """Choose according to PIECE_SPEC rule 6.2, 1-4"""
    pitches = set() # use set to avoid duplicates
    for color, share in shares.items():
        if share > INCLUDE_PCENT_LINE:
            included = True
        else:
            included = random.random() < share
        
        if not included:
            continue
        # print(color)
        
        low_pitch, high_pitch = COLOR_INTERVAL_MAP[color]
        if share > MAJORITY_PCENT_LINE:
            if random.random() < 0.5:
                pitches.update((low_pitch, high_pitch))
            else: pitches.add(random.choice((low_pitch, high_pitch)))
        else:
            pitches.update((low_pitch, high_pitch))
    return pitches

def get_sorted_chord(pitches, registers):
    """Place pitches in their fixed registers and return MIDI numbers from low to high"""
    chord = []
    for pitch in pitches:
        chord.append(get_midi_num(pitch, registers[pitch]))
        
    sorted_chord = sorted(chord) # hands back a sorted ver of chord notes
    return sorted_chord

def generate_notes(votes_count: dict[str, int], registers: dict[str, int]):
    """Turns audience votes count into a sorted chord of midi numbers. Called by server.py"""
    shares = votes_to_shares(votes_count)
    if shares is None:
        pitches = set()
    else:
        pitches = choose_pitches(shares)
        
    if not pitches: # whether the pitches set is empty
        pitches = {random.choice(DORIAN_SCALE)}
    
    return get_sorted_chord(pitches, registers)
    


    
        
    
