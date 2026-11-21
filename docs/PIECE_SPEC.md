- What the audience chooses:
    A bunch of colored bottons. They can press one at a time, and that will be the contribution that they make. 
    The idea is almost like creating a combined color palette every now and then as the piece goes, that changes 
    the pitches musicians are seeing on the score. Audience and musicians will both see the corresponding text 
    instructions (text score). 
    
    The only thing is that, just like a game, I will initiate a room and the audience will select [YES] or [NO] 
    under "join the experience?". Once they start making their decisions, I from the console side will be able 
    to see how many audience have joined, and when I see enough people joined in, I'll press [Start Piece], to 
    lock people from connecting in. 

    Then they will be given 10-15 seconds (depending on the length of the sentence they see) to vote for a color 
    while seeing one line of instruction. They will see "what color do you associate with the following sentence?" 
    and the one line written text which belongs to the text score musicians have to base on while doing improvisations. 
    Then as the musicians start to respond on stage, the globle clock will move the piece forward to the upcoming 
    section (selection screens). Always the audience will foresee the next line of text (text score), vote for a 
    colored bottom during count down, and the musicians will then see the line of text that the audience just saw with 
    the updated musical score reflecting audience's choices, and respond with improvisations. 

    Towards the middle (0.618 of an 8-min piece), audience's phone are going to start gradually making long warm sine tones
    of select notes on the score that's on the screen live. Each phone is allowed to sound one randomly assigned pitch, so 
    the phone is doubling the octet in parts of the harmony in real time. Not all the phones can double the quartet 
    all the time. As the piece runs, the system will select a growing random number of audience members for them to click 
    [Make a sound]. The number of audience who are allowed to do that grows as the piece goes, and at the end all 
    participating audience plays with the octect doing tutti, and the final screen as one last bottom to select, the piece
    goes back to where it started. 

- What changes in the notations:
    Performers are free to use any articulations, dynamics, and rhythms to help them improvise. The only rule is that they
    can only use pitches showing up on the screen while improvising. The audience's choices of colored bottoms are  
    converted live to harmonies written in chorale style chords on the performer's iPad's, and the audience's choices 
    only changes what shows up as pitches in the form of harmonies (vertical chords without stem).

- How audience's votes get converted to notated pitches:
   Audience will see 7 colored bottons, each represent an interval from the dorian mode scale (they will only see the color 
    bottons without knowing what they represent when choosing them). The color - interval pairs are:
        Color	Span	Interval
        Red	    D–E	    whole tone
        Orange	E–F	    semitone
        Yellow	F–G	    whole tone
        Green	G–A	    whole tone
        Blue	A–B	    whole tone
        Indigo	B–C	    semitone
        Violet	C–D	    whole tone

    (according to Newton's Opticks Book I, Part II, Prop. VI)

    According to this color mapping, the pitches show up on the score depends on the percentage of the represented colors get
    chosen. The higher the percentage is, the higher possibility the represented interval appears. The actual pitches appear-
    ing on the score can be anything from a single note to all 7 notes together.

- Audience will always submit their votes during the 10-15 sec count down, and once their choice is submited(I should know),
     The score updates when I trigger it from the concole. 

- Operation pipeline:
    Beginning of the piece:
    1. I press [Piece Start] audience stop joining in, the globle clock starts moving

    For every page of score: 
    // n = 1; n<pageNum; n++;
    1. Audience have 10-15 sec countdown to select a color button to generate notes on page n
    2. I see "Audience voting completed!" message, press X from the console to export the newly generated notation to
    musicians' screens for them to play. Meanwhile the iPads show line n+1 plus chord n+1, with countdown for audience.
    3. The countdown ends, I wait to decide when to press X to export a new page of pitches for the iPads. 

    Audiences and I are not allowed to generate new pages when there are only less than 10sec left for the piece (fixed to
    8 min).

    The text will be 16 - 20 lines, distributed relatively evenly throughtout the piece.  

    When the piece is in 10 sec count down, whatever shows up as page 1 of the piece returns exactly the same (ends how it
    started)

- Joining and locking for audiences:
    If an audience press "NO" during the begining joining and locking stage before piece starts, on their screen it prints 
    "Thank you for your response! Please sit back and enjoy the performance."

    If an audience arrives after the piece has started and tries to join, it prints "The piece has started. Please sit 
    back and enjoy the performance."

    If a phone drops out mid piece due to accidental events: each phone saves a random ID when it joins, and after Piece
    Start the server lets in only IDs it already knows. 

- Phone Pitch Assignment: re-drawn at each update from the current chord.

- What "make a sound" does for audience: audience press, hold, and release for the sound to fade in, stay, and fade out. The 
    fade in and fade out should be pretty gentle curves (random between 0.25-1sec both ways).

- Pitch range:
    If a pitch is lower than B3 in the notation, the phone's pitch rounds back up an octave. The upperbound for phone pitch
    is C7. 

    The score on iPads can show pitches between C3-C6, but the string octect is free to take the pitch and play in any 
    octave. 

- The players are looking at a grand staff paper with pitches in stem-less quarter notes written as chords. The number of 
    pitches showing at a time ranges from one note to 7 notes, and the players are free to select any pitch(es) while 
    actively listening to the rest of the room and the ensemble. 

- The phones don't make sound from the beginning, but starting 61.8% into the piece(4'57"), select audience's can start to 
    choose whether they want to make a sound or not. Each screen updates randomly choose a sample of participating audience
    to give them the opportunity to make a sound if they choose to, and by second to the last score update of the piece, 
    all the participating audience will be allowed to make a sound. The sample of audience who are allowed to choose to make
    a sound grows exponentially as the piece goes, from [5%-20%] to [80%-100%]. So there should be an automated lottery 
    process deciding which audience's phone gets an opportunity to make a sound. The system should make sure every partici-
    pating audience member gets at least one chance to choose to make a sound or not by the end of the piece.     
      
