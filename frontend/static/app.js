document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const chatBox = document.getElementById("chatBox");
    const queryInput = document.getElementById("queryInput");
    const sendBtn = document.getElementById("sendBtn");
    const docList = document.getElementById("docList");

    // 🧠 Backend Flask API base URL
    const API_BASE = "http://127.0.0.1:5000";

    // ✅ Load existing document metadata
    async function loadMetadata() {
        try {
            const res = await fetch(`${API_BASE}/metadata`, { method: "GET" });
            if (!res.ok) throw new Error("Failed to fetch metadata");
            const docs = await res.json();

            docList.innerHTML = "";
            docs.forEach(d => {
                const li = document.createElement("li");
                li.textContent = d.filename;
                li.classList.add("doc-item");
                docList.appendChild(li);
            });
        } catch (err) {
            console.error("Error loading metadata:", err);
        }
    }

    loadMetadata();

    // ✅ Upload document
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) return alert("Please select a file first.");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`${API_BASE}/upload`, {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const errorText = await res.text();
                console.error("Upload failed:", errorText);
                return alert("❌ Upload failed. Check backend logs.");
            }

            alert("✅ File uploaded successfully!");
            fileInput.value = "";
            loadMetadata();
        } catch (err) {
            console.error("Error uploading file:", err);
            alert("⚠️ Cannot connect to backend (port 8000).");
        }
    });

    // ✅ Send user query
    async function sendMessage() {
        const text = queryInput.value.trim();
        if (!text) return;

        addMessage("user", text);
        queryInput.value = "";

        // Typing indicator
        const typing = addMessage("bot", "🤔 Thinking...");

        try {
            const response = await fetch(`${API_BASE}/query`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: text })
            });

            chatBox.removeChild(typing);

            if (response.ok) {
                const data = await response.json();
                addMessage("bot", data.answer || "No response found.");
            } else {
                addMessage("bot", "⚠️ Error processing query.");
            }
        } catch (err) {
            console.error("Error:", err);
            chatBox.removeChild(typing);
            addMessage("bot", "🚫 Backend server not reachable.");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    queryInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    // ✅ ChatGPT-style message rendering
    function addMessage(sender, text) {
        const msg = document.createElement("div");
        msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");
        avatar.textContent = sender === "user" ? "🧑‍💻" : "🤖";

        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.textContent = text;

        msg.appendChild(avatar);
        msg.appendChild(bubble);
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
        return msg;
    }
});
