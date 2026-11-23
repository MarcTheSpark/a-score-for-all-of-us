"use strict";

let socket = null;   // created only when an audience presses YES

// Show only one screen, hide all the others
const SCREENS = ["joinScreen", "declinedScreen", "waitScreen", "lockedScreen"];
function showScreen(id) {
    for (const screen of SCREENS) {
        document.getElementById(screen).hidden = (screen !== id);
    }
}

// YES - connect and join the room
document.getElementById("yes").addEventListener("click", () => {
    socket = new WebSocket(SERVER_URL);

    socket.addEventListener("open", () => {
        socket.send(JSON.stringify({ type: "hello", role: "audience" }));
        showScreen("waitScreen");
    });

    socket.addEventListener("message", (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "locked") {
            showScreen("lockedScreen");
        }
    });
});

// NO - never connect to the room
document.getElementById("no").addEventListener("click", () => {
    showScreen("declinedScreen");
});
