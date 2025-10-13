document.addEventListener('DOMContentLoaded', function() {
    // -------------------------------
    // DOM Elements
    // -------------------------------
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadStatus = document.getElementById('uploadStatus');
    const dropArea = document.getElementById('dropArea');
    const fileList = document.getElementById('fileList');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatWindow = document.getElementById('chatWindow');
    const typingIndicator = document.getElementById('typingIndicator');

    // Backend base URL
    const BACKEND_URL = "http://127.0.0.1:8000";

    // Sample uploaded files list
    const sampleFiles = [];

    // Initialize file list
    updateFileList();

    // -------------------------------
    // File Upload Handler
    // -------------------------------
    uploadBtn.addEventListener('click', async function(e) {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            showUploadStatus('Please select a file first.', 'error');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        showUploadStatus(`Uploading ${file.name}...`, 'info');

        try {
            const response = await fetch(`${BACKEND_URL}/upload`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) throw new Error(`Upload failed with status ${response.status}`);

            const result = await response.json();
            showUploadStatus(`✅ Successfully uploaded ${file.name}`, 'success');

            sampleFiles.push({ name: file.name, size: formatFileSize(file.size) });
            updateFileList();
            fileInput.value = ''; // Reset file input
        } catch (error) {
            console.error("Upload error:", error);
            showUploadStatus(`❌ Error uploading file: ${error.message}`, 'error');
        }
    });

    // -------------------------------
    // Drag & Drop File Support
    // -------------------------------
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.style.borderColor = 'var(--primary)';
        dropArea.style.backgroundColor = 'rgba(67, 97, 238, 0.1)';
    }

    function unhighlight() {
        dropArea.style.borderColor = 'var(--gray-light)';
        dropArea.style.backgroundColor = '';
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;

        if (files.length > 0) {
            showUploadStatus(`Ready to upload ${files[0].name}`, 'info');
        }
    }

    // -------------------------------
    // Chat Q&A Handler
    // -------------------------------
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        chatInput.value = '';

        typingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch(`${BACKEND_URL}/query`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message }),
            });

            const data = await response.json();
            typingIndicator.style.display = 'none';

            if (data.answer) {
                addMessage(data.answer, 'bot');
            } else {
                addMessage("⚠️ No relevant information found in the uploaded documents.", 'bot');
            }
        } catch (error) {
            typingIndicator.style.display = 'none';
            console.error("Query error:", error);
            addMessage("❌ Error connecting to backend. Check console/logs.", 'bot');
        }
    });

    // -------------------------------
    // Helper Functions
    // -------------------------------
    function showUploadStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = 'upload-status';
        uploadStatus.classList.add(`status-${type}`);
        uploadStatus.style.display = 'block';

        // Auto-hide success messages
        if (type === 'success') {
            setTimeout(() => {
                uploadStatus.style.display = 'none';
            }, 5000);
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function updateFileList() {
        fileList.innerHTML = '';

        sampleFiles.forEach(file => {
            const li = document.createElement('li');
            li.className = 'file-item';
            li.innerHTML = `
                <i class="fas fa-file-pdf"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${file.size}</span>
                <div class="file-actions">
                    <button class="file-action" title="View"><i class="fas fa-eye"></i></button>
                    <button class="file-action" title="Delete"><i class="fas fa-trash"></i></button>
                </div>
            `;
            fileList.appendChild(li);
        });
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageText = document.createElement('p');
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();

        messageDiv.appendChild(messageText);
        messageDiv.appendChild(messageTime);

        chatWindow.insertBefore(messageDiv, typingIndicator);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
});


