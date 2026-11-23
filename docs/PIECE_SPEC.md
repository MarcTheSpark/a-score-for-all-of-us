# A Score for All of Us: Piece Spec

## 1. Overview

A piece for string octet and audience, fixed to 8 min.

The audience will see a bunch of colored buttons (7 buttons). They can press one at a time, and that will be the contribution that they make. The idea is almost like creating a combined color palette every now and then as the piece goes, that changes the pitches musicians are seeing on the score. Audience and musicians will both see the corresponding text instructions (text score).

Performers are free to use any articulations, dynamics, and rhythms to help them improvise. The only rule is that they can only use pitches showing up on the screen while improvising.

Towards the middle (61.8% of the piece, 4'57"), audience's phones are going to start gradually making long warm sine tones of select notes on the score that's on the screen live, so the phones are doubling the octet in parts of the harmony in real time. At the end all participating audience plays with the octet doing tutti, and the final screen will be the same as the first screen: the piece goes back to where it started.

## 2. Guiding Chart

| People | Device | What they see |
|---|---|---|
| Audience | Their phones (QR code) | Join screen, then one line of text + 7 colored buttons + countdown; later a [Make a sound] button |
| Octet | iPads | The current line of text + the current chord on a grand staff |
| Me | Console | How many audience have joined, [Start Piece], "Audience voting completed!", button X |

## 3. Form and timeline

- The piece is fixed to 8 min. The global clock starts when I press [Start Piece].
- The text will be 16 - 20 lines, distributed relatively evenly throughout the piece. Each line is one page of score.
- 0'00" – 4'57": audience votes; phones make no sound.
- 4'57" (61.8%): select audience members can start to make a sound (see Section 7).
- 7'30": all participating audience are allowed to make a sound.
- Last 10 sec: audience and I are not allowed to generate new pages. Whatever showed up as page 1 of the piece returns exactly the same (ends how it started).
- If the 16-20 lines run out first, just keep the last page until it's time to return to the beginning.
- If the 8 min run out first, just turn to the beginning page without showing the rest.
- The final screen is the same as the first voting screen (the first time pitches are on the grand staff). On the phones, line 1 is shown again for reading only.

## 4. Joining and locking

Just like a game, I will initiate a room and the audience will select [YES] or [NO] under "Join the experience?". Once they start making their decisions, I from the console side will be able to see how many audience have joined, and when I see enough people joined in, I'll press [Start Piece], to lock people from connecting in.

- If an audience member presses [NO] during the joining stage before the piece starts, their screen prints: "Thank you for your response! Please sit back and enjoy the performance."
- If an audience member arrives after the piece has started and tries to join, it prints: "The piece has started. Please sit back and enjoy the performance."
- If a phone drops out mid piece due to accidental events: each phone saves a random ID when it joins, and after [Start Piece] the server lets in only IDs it already knows.

## 5. Operation pipeline

The audience will always foresee the next line of text (text score) and vote for a colored button during the countdown. The musicians will then see the line of text that the audience just saw, with the updated musical score reflecting the audience's choices, and respond with improvisations.

**Beginning of the piece:**

1. I press [Start Piece]: audience stop joining in, the global clock starts moving.

**For every page of score** (`n = 1; n < pageNum; n++`):

0. During the very first vote, before page 1 exists, the iPads show an empty staff paper.
1. Audience have a 10-15 sec countdown (determined by the number of characters in each line: 50 and less gives 10 sec, 100 and more gives 15 sec, scaled evenly in between) to select a color button to generate notes on page n. They see "What color do you associate with the following sentence?" and line n.
2. I see "Audience voting completed!" and press X from the console to export the newly generated notation to the musicians' screens for them to play. Meanwhile the iPads show line n plus chord n, with a countdown for the audience to vote for pitches on the upcoming page. X can only be pressed after I see "Audience voting completed!" on my screen.
3. The countdown ends, I wait to decide when to press X to export a new page of pitches for the iPads.

Audience will always submit their votes during the 10-15 sec countdown, and once their choice is submitted, I should know. The score updates only when I trigger it from the console.

## 6. From votes to notated pitches

### 6.1 Color - interval mapping

Audience will see 7 colored buttons, each representing an interval from the Dorian mode scale (they will only see the color buttons without knowing what they represent when choosing them).

| Color | Pitch | Interval |
|---|---|---|
| Red | D–E | whole tone |
| Orange | E–F | semitone |
| Yellow | F–G | whole tone |
| Green | G–A | whole tone |
| Blue | A–B | whole tone |
| Indigo | B–C | semitone |
| Violet | C–D | whole tone |

(according to Newton's *Opticks*, Book I, Part II, Prop. VI)

The pitches showing up on the score depend on the percentage each color gets chosen. The higher the percentage is, the higher the possibility the represented interval appears. The actual pitches appearing on the score can be anything from a single note to all 7 notes together.

### 6.2 Rules, in order

1. Any color (interval) above 15% gets included.
2. Each remaining interval is drawn with a probability equal to its vote share.
3. When any color is over 50%, there is a 50% chance of both notes in the mapped interval being added to the score, and a 50% chance of either one of the pitches in concern being added to the score. Every other included interval adds both of its pitches.
4. One pitch class only appears once, so the doublings are fully left to the performers.
5. When the chord comes out empty, show ONE random pitch so that the players play in unison.

### 6.3 Register

At each run of the piece, every pitch is assigned a fixed register randomly, within C3-C6, and it never changes for the run of the piece. The score, written in chorale style, places each pitch in its fixed register.

## 7. Notation on the iPads

The players are looking at grand staff paper with pitches in stem-less quarter notes written as chords (vertical chords without stems). The number of pitches showing at a time ranges from one note to 7 notes, and the players are free to select any pitch(es) while actively listening to the rest of the room and the ensemble.

The score on the iPads shows pitches between C3-C6, but the string octet is free to take the pitch and play in any octave. The audience's choices only change what shows up as pitches in the form of harmonies.

iPads are used in landscape orientation.

## 8. Phone sound and lottery

### 8.1 Lottery

The phones don't make sound from the beginning, but starting 61.8% into the piece (4'57"), select audience members can start to choose whether they want to make a sound or not. Not all the phones can double the octet all the time.

- Each score update randomly chooses a sample of participating audience to give them the opportunity to make a sound if they choose to.
- The sample of audience who are allowed to make a sound grows exponentially as the piece goes, from [5%-20%] to [80%-100%] from 4'57" to 7'30". The starting share is picked at random between [5%-20%].
- By 7'30", all the participating audience will be allowed to make a sound.
- So there should be an automated lottery process deciding which audience's phone gets an opportunity to make a sound. The system should make sure every participating audience member gets at least one chance to choose to make a sound or not by the end of the piece.

### 8.2 Pitch assignment

Each phone is allowed to sound one randomly assigned pitch, re-drawn at each update from the current chord.

### 8.3 What [Make a sound] does

Audience press, hold, and release for the sound to fade in, stay, and fade out. The fade in and fade out should be pretty gentle curves (random between 0.25-1 sec both ways).

- A tone from the phone crossfades to the new pitch if an audience member is holding while a page changes.
- If a phone was allowed on the last page but not this one and the person is still holding, the pitch fades out as if they just released it.

### 8.4 Phone pitch range

If a pitch is lower than B3 in the notation, the phone's pitch rounds back up an octave. The upper bound for phone pitch is C7.

## 9. Messages

All messages are JSON objects with a "type" field.

| Message | Direction | Meaning |
|---|---|---|
| hello with role: "audience" | phone -> server | sent when an audience member presses YES |
| room | server -> console | {"type": "room", "joined": 12, "started": false} |
| start_piece | console -> server | Composer press Start Piece | 
| locked | server -> phone | "The piece has started," sent to a late YES from the audience |  

### score
**Direction:** server -> iPads
**When:** at [Start Piece] (page 0, empty staff paper); then each time I press X

| Field | Type | Notes |
|---|---|---|
| type | string | always "score" |
| page | integer | page number, starting at 1; 0 = empty staff paper before the first page |
| text | string | the text for the current page |
| chord | list of integers | MIDI numbers, low to high, range 48–84; empty list for page 0 |

**Examples:**
```json
{"type": "score", "page": 3, "text": "…", "chord": [50, 62, 67, 81]}
```
```json
{"type": "score", "page": 0, "text": "", "chord": []}
```
```json
{"type": "hello", "role": "score"}
```

### hello
**Direction:** any client -> server
**When:** right after connecting, as the first message

| Field | Type | Notes |
|---|---|---|
| type | string | always "hello" |
| role | string | "score" (iPads), "console" (me); later "audience" (phones) |
| key | string | console only; must match the server's CONSOLE_KEY (set on Render) |

**Example:**
```json
{"type": "hello", "role": "score"}
```

### next_page
**Direction:** console -> server
**When:** I press X

| Field | Type | Notes |
|---|---|---|
| type | string | always "next_page" |
| counts | object | color name → number of votes; color names spelled as in generator.py ("Red", "Orange", …) |

**Example:**
```json
{"type": "next_page", "counts": {"Red": 3, "Orange": 0, "Yellow": 0, "Green": 1, "Blue": 0, "Indigo": 0, "Violet": 0}}
```

**Server response:** builds the next page with generate_notes and broadcasts a `score` message to every score page.
