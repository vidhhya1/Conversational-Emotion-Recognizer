
const recordButton = document.getElementById('recordButton');
const emotionStatus = document.getElementById('emotionStatus');
const chatBox = document.getElementById('chatBox');


let isRecording = false;
let mediaRecorder;
let socket;
let currentUserMessageElement = null; 


const SILENCE_THRESHOLD_MS = 5000; 
let silenceTimer;


function setupWebSocket() {
    socket = new WebSocket('ws://localhost:5000/ws');

    socket.onopen = () => {
        console.log('WebSocket connection established.');
        addMessage('Connected to the server.', 'system');
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'interim_transcript') {
            if (currentUserMessageElement) {
                currentUserMessageElement.querySelector('p').textContent = data.text;
            }
        } else if (data.type === 'final_response') {

            if (currentUserMessageElement) {
                currentUserMessageElement.querySelector('p').textContent = data.user_text;
            }
            currentUserMessageElement = null; 

        
            const audioBlob = new Blob([new Uint8Array(atob(data.audio).split("").map(char => char.charCodeAt(0)))], { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();

        
            addMessage(data.bot_text, 'bot');

            emotionStatus.textContent = data.emotion;
        }
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed.');
        addMessage('Connection lost. Please refresh.', 'system');
        currentUserMessageElement = null; 
        clearTimeout(silenceTimer); 
    };

    socket.onerror = (error) => {
        console.error('WebSocket Error:', error);
        addMessage('An error occurred with the connection.', 'system');
        currentUserMessageElement = null; 
        clearTimeout(silenceTimer); 
    };
}

async function setupMediaRecorder() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        addMessage('Media Devices API not supported.', 'system');
        return;
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0 && socket && socket.readyState === WebSocket.OPEN) {
                socket.send(event.data);
                resetSilenceTimer(); 
            }
        };

        mediaRecorder.onstart = () => {
            currentUserMessageElement = addMessage('Listening...', 'user');
            resetSilenceTimer();
        };

        mediaRecorder.onstop = () => {
    
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ event: 'end_of_speech' }));
            }
            clearTimeout(silenceTimer); 
        };

    } catch (err) {
        console.error('Error accessing microphone:', err);
        addMessage('Could not access microphone. Please grant permission.', 'system');
    }
}


function resetSilenceTimer() {
    clearTimeout(silenceTimer); 
    silenceTimer = setTimeout(() => {
        console.log('Silence detected for', SILENCE_THRESHOLD_MS / 1000, 'seconds. Stopping recording.');
        if (isRecording) { 
            toggleRecording(); 
        }
    }, SILENCE_THRESHOLD_MS);
}

function toggleRecording() {
    if (!mediaRecorder) {
        addMessage('Microphone is not set up.', 'system');
        return;
    }

    isRecording = !isRecording;
    if (isRecording) {
       
        mediaRecorder.start(500);
        recordButton.classList.add('recording');
    
    } else {
        mediaRecorder.stop();
        recordButton.classList.remove('recording');
        
    }
}

function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-bubble', sender);

    const textElement = document.createElement('p');
    textElement.textContent = text;
    messageElement.appendChild(textElement);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
    return messageElement; 
}

recordButton.addEventListener('click', toggleRecording);

window.onload = () => {
    setupMediaRecorder();
    setupWebSocket();
};