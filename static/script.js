// Global variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// DOM Elements
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const messagesDiv = document.getElementById('messages');
const languageSelect = document.getElementById('language');
const recordingStatus = document.getElementById('recordingStatus');
const darkModeToggle = document.getElementById('darkMode');
const autoPlayToggle = document.getElementById('autoPlay');

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        sendMessage();
    }
});

recordBtn.addEventListener('click', startRecording);
stopBtn.addEventListener('click', stopRecording);
darkModeToggle.addEventListener('change', toggleDarkMode);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSpeech();
    showWelcomeMessage();
});

// Dark Mode
function toggleDarkMode(e) {
    if (e.target.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.removeItem('darkMode');
    }
}

// Load saved preferences
window.addEventListener('load', () => {
    if (localStorage.getItem('darkMode')) {
        darkModeToggle.checked = true;
        document.body.classList.add('dark-mode');
    }
    if (localStorage.getItem('autoPlay') === 'false') {
        autoPlayToggle.checked = false;
    }
});

// Web Speech API
function initializeWebSpeech() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        recordBtn.disabled = true;
        recordBtn.title = 'Speech Recognition not supported in your browser';
        return;
    }

    // Check for MediaRecorder API
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        recordBtn.disabled = true;
        recordBtn.title = 'Microphone access not available';
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        isRecording = true;

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            transcribeAudio(audioBlob);
        };

        mediaRecorder.start();
        recordBtn.style.display = 'none';
        stopBtn.style.display = 'flex';
        recordingStatus.classList.add('active');
        recordingStatus.textContent = '🔴 Recording... Click Stop to finish';
    } catch (error) {
        console.error('Error accessing microphone:', error);
        recordingStatus.classList.add('active');
        recordingStatus.textContent = '❌ Microphone access denied';
        recordingStatus.style.background = '#f8d7da';
        recordingStatus.style.color = '#721c24';
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        isRecording = false;
        recordBtn.style.display = 'flex';
        stopBtn.style.display = 'none';
        recordingStatus.classList.remove('active');
        recordingStatus.textContent = '';
    }
}

async function transcribeAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('language', getLanguageCode());

    recordingStatus.classList.add('active');
    recordingStatus.textContent = '⏳ Transcribing audio...';

    try {
        const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        recordingStatus.classList.remove('active');
        recordingStatus.textContent = '';

        if (data.success) {
            userInput.value = data.transcript;
            sendMessage();
        } else {
            showErrorMessage('Failed to transcribe audio: ' + data.error);
        }
    } catch (error) {
        console.error('Transcription error:', error);
        recordingStatus.classList.remove('active');
        recordingStatus.textContent = '';
        showErrorMessage('Error transcribing audio: ' + error.message);
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }

    // Add user message to UI
    addMessageToUI(message, 'user');
    userInput.value = '';
    sendBtn.disabled = true;
    recordBtn.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                language: languageSelect.value
            })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.success) {
            addMessageToUI(data.response, 'bot');
            // Auto-play response if enabled
            if (autoPlayToggle.checked) {
                speakMessage(data.response);
            }
        } else {
            showErrorMessage('Error: ' + (data.error || 'Unknown error occurred'));
        }
    } catch (error) {
        removeTypingIndicator();
        console.error('Chat error:', error);
        showErrorMessage('Error: ' + error.message);
    } finally {
        sendBtn.disabled = false;
        recordBtn.disabled = false;
    }
}

function addMessageToUI(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const currentTime = new Date().toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    messageDiv.innerHTML = `
        ${escapeHtml(message)}
        <div class="message-time">${currentTime}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    messagesDiv.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message bot-message';
    errorDiv.style.background = '#f8d7da';
    errorDiv.style.color = '#721c24';
    errorDiv.innerHTML = `
        ❌ ${escapeHtml(message)}
        <div class="message-time">${new Date().toLocaleTimeString()}</div>
    `;
    
    messagesDiv.appendChild(errorDiv);
    scrollToBottom();
}

function scrollToBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showWelcomeMessage() {
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message bot-message';
    welcomeDiv.style.background = '#e8f5e9';
    welcomeDiv.style.color = '#2e7d32';
    welcomeDiv.innerHTML = `
        <strong>👋 Welcome to Sarvam AI Assistant!</strong><br><br>
        I'm here to help you learn about Sarvam AI's products and services:<br><br>
        ✅ <strong>Speech-to-Text (Saaras v3)</strong> - 23 language support<br>
        ✅ <strong>Text-to-Speech (Bulbul v3)</strong> - Natural voice generation<br>
        ✅ <strong>Sarvam-M LLM</strong> - Advanced multilingual AI<br>
        ✅ <strong>Samvaad Studio</strong> - Conversational AI agents<br>
        ✅ <strong>Vision/Document Intelligence</strong> - Content extraction<br><br>
        Try asking me about any of these features or Sarvam AI in general!
        <div class="message-time">Assistant</div>
    `;
    
    messagesDiv.appendChild(welcomeDiv);
    scrollToBottom();
}

function getLanguageCode() {
    const languageMap = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'kn': 'kn-IN',
        'ml': 'ml-IN',
        'mr': 'mr-IN',
        'gu': 'gu-IN',
        'bn': 'bn-IN',
        'pa': 'pa-IN'
    };
    
    return languageMap[languageSelect.value] || 'en-IN';
}

function speakMessage(message) {
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = languageSelect.value + '-IN';
    utterance.rate = 0.9;
    
    window.speechSynthesis.speak(utterance);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Health check on load
window.addEventListener('load', () => {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => console.log('API Status:', data))
        .catch(error => console.error('API connection error:', error));
});
