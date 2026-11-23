"use strict";

const COLORS = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"];
const socket = new WebSocket(SERVER_URL);

socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ type: "hello", role: "console" }));
});

socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "score") {
        document.getElementById("status").textContent =
            `Page ${message.page}: ${message.text}`;
    }
});

document.getElementById("next").addEventListener("click", () => {
    const counts = {};
    for (const color of COLORS) {
        counts[color] = Number(document.getElementById(color).value);
    }
    socket.send(JSON.stringify({ type: "next_page", counts: counts }));
});
