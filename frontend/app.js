const backendURL = "http://127.0.0.1:8000";

// ---------------- File Upload ----------------
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) return alert("Please select a file!");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const statusDiv = document.getElementById("uploadStatus");
    statusDiv.textContent = "Uploading...";

    try {
        const response = await fetch(`${backendURL}/upload`, {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        statusDiv.textContent = data.message || "Upload success!";
    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Upload failed. Cannot connect to backend.";
    }
});

// ---------------- Chat Functionality ----------------
const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";

    try {
        const response = await fetch(`${backendURL}/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: message }),
        });
        const data = await response.json();
        addMessage("bot", data.answer || "No response from backend.");
    } catch (err) {
        console.error(err);
        addMessage("bot", "Cannot connect to backend.");
    }
});

// ---------------- Helper Function ----------------
function addMessage(sender, message) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("chat-message", sender === "user" ? "user-msg" : "bot-msg");
    msgDiv.textContent = message;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
