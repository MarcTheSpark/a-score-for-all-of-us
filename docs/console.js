"use strict";

const COLORS = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"];
const CONSOLE_KEY = location.hash.slice(1);   // the text after "#"
const socket = new WebSocket(SERVER_URL);

//  Read the seven color boxes into {color: count}
function readCounts() {
    const counts = {};
    for (const color of COLORS) {
        counts[color] = Number(document.getElementById(color).value);
    }
    
    return counts;
}

socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ type: "hello", role: "console", key: CONSOLE_KEY }));
});

socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "score") {
        document.getElementById("status").textContent =
            `Page ${message.page}: ${message.text}`;
    }
});

// X cues next page
document.getElementById("next").addEventListener("click", () => {
    socket.send(JSON.stringify({ type: "next_page", counts: readCounts() }));
});

//Go to any page
document.getElementById("goTo").addEventListener("click", () => {
    const page = Number(document.getElementById("pageInput").value);
    socket.send(JSON.stringify({type: "go_to_page", page: page, counts: readCounts()}));
});
