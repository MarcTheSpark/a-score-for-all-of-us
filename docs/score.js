"use strict";

// Pull classes needed out of VexFlow
const { Renderer, Stave, StaveConnector } = VexFlow;

function drawScore(message) {
    // text line
    const textElement = document.getElementById("text");
    textElement.textContent = message.text;

    // render + context
    const scoreDiv = document.getElementById("score");
    const renderer = new Renderer(scoreDiv, Renderer.Backends.SVG);
    renderer.resize(window.innerWidth, window.innerWidth - 200);
    const context = renderer.getContext();

    // two staves with clefs
    const treble = new Stave(150, 40, 1000);
    treble.addClef("treble");
    treble.setContext(context).draw();

    const bass = new Stave(150, 150, 1000);
    bass.addClef("bass");
    bass.setContext(context).draw();

    // left line + brace
    const leftLine = new StaveConnector(treble, bass);
    leftLine.setType("singleLeft");
    leftLine.setContext(context).draw();
 
    const brace = new StaveConnector(treble, bass);
    brace.setType("brace");
    brace.setContext(context).draw();
}

// Font-loading pattern adapted from the VexFlow 5 getting-started guide:
// https://vexflow.github.io/vexflow-examples/guides/getting-started/
VexFlow.loadFonts('Bravura', 'Academico').then(() => {
    VexFlow.setFonts('Bravura', 'Academico');
    console.log("ready");
    drawScore({ type: "score", page: 0, text: "Test line", chord: [] });
});


