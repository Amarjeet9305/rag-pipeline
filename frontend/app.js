document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadStatus = document.getElementById('uploadStatus');
    const dropArea = document.getElementById('dropArea');
    const fileList = document.getElementById('fileList');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatWindow = document.getElementById('chatWindow');
    const typingIndicator = document.getElementById('typingIndicator');
    
    // Sample uploaded files for demonstration
    const sampleFiles = [
        { name: 'Research_Paper.pdf', size: '2.4 MB' },
        { name: 'Project_Report.docx', size: '1.1 MB' }
    ];
    
    // Initialize file list
    updateFileList();
    
    // Upload button click handler
    uploadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (fileInput.files.length === 0) {
            showUploadStatus('Please select a file first.', 'error');
            return;
        }
        
        // Simulate file upload
        const file = fileInput.files[0];
        showUploadStatus(`Uploading ${file.name}...`, 'info');
        
        setTimeout(() => {
            showUploadStatus(`Successfully uploaded ${file.name}`, 'success');
            sampleFiles.push({ name: file.name, size: formatFileSize(file.size) });
            updateFileList();
            fileInput.value = ''; // Reset file input
        }, 1500);
    });
    
    // Drag and drop functionality
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
    
    // Chat form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        chatInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        // Simulate bot response after delay
        setTimeout(() => {
            typingIndicator.style.display = 'none';
            
            // Generate a sample response
            const responses = [
                "Based on the document you uploaded, I can tell you that...",
                "The document mentions several key points about this topic...",
                "I've analyzed your document and found the following information...",
                "According to the content in your uploaded file..."
            ];
            
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addMessage(randomResponse + " This is a simulated response. In a real RAG system, this would be generated based on your document's content.", 'bot');
        }, 2000);
    });
    
    // Helper functions
    function showUploadStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = 'upload-status';
        uploadStatus.classList.add(`status-${type}`);
        uploadStatus.style.display = 'block';
        
        // Auto-hide success messages after 5 seconds
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
                    <button class="file-action" title="View">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="file-action" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
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