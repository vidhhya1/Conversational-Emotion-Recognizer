# 🗣️ Conversational Emotion Recognizer (Advanced AI Companion)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-Flask--Sock-lightgrey?style=flat-square)](https://flask-sock.readthedocs.io/en/latest/)
[![Google Gemini API](https://img.shields.io/badge/Google-Gemini%20API-orange?style=flat-square&logo=google)](https://ai.google.dev/gemini-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Project Overview

The **Conversational Emotion Recognizer** is an advanced AI-powered companion designed to understand and respond to human emotions in real-time spoken conversations. By automating the analysis of sentiment and tone, this system aims to provide empathetic and contextually appropriate audio responses, enhancing human-AI interaction.

This project goes beyond simple text processing, leveraging cutting-edge AI models for robust Speech-to-Text, fine-grained Emotion Detection, intelligent Response Generation, and realistic Text-to-Speech, all delivered through a seamless web interface.

## 🚀 Features

* **🎙️ Real-time Speech-to-Text (STT):** Converts user's spoken audio into text on the fly using OpenAI's powerful Whisper model.
* **❤️ Advanced Emotion Detection:** Analyzes the transcribed text to identify a user's mood (e.g., Happy, Sad, Surprised, Angry, Anxious, Neutral) using a fine-tuned Hugging Face Transformers model.
* **🧠 Emotion-Aware Response Generation:** Utilizes the Google Gemini Pro API to generate empathetic, supportive, and contextually relevant text responses based on the detected emotion and user's input.
* **🗣️ Text-to-Speech (TTS) Output:** Converts the AI's generated response back into natural-sounding speech using Google's Text-to-Speech (gTTS) and pydub.
* **⚡ Real-time Interaction:** A responsive web interface facilitates smooth, near-instantaneous conversational turns.
* **🕒 Automatic End-of-Speech Detection:** Intelligently detects pauses in user speech (e.g., 5 seconds of silence) to automatically stop recording and initiate processing.
* **🌐 Web-based Interface:** Accessible and user-friendly chat interface in your browser.

## ⚙️ Architecture & How It Works

The project follows a client-server architecture using WebSockets for real-time communication: 
+----------------+       WebSocket       +---------------------+
|    Frontend    |<--------------------->|       Backend       |
| (index.html,   |    (Audio Chunks)     |      (Flask)        |
|  script.js,    |                       |                     |
|  style.css)    |                       | +-----------------+ |
| - Records audio|                       | |  STT (Whisper)  | |
| - Displays chat|                       | | - Transcribes   | |
| - Plays audio  |                       | |   audio chunks  | |
|                |                       | +-----------------+ |
|                |                       |                     |
|                |                       | +-----------------+ |
|                |                       | | Emotion Model   | |
|                |                       | | (Transformers)  | |
|                |                       | | - Detects mood  | |
|                |                       | +-----------------+ |
|                |                       |                     |
|                |                       | +-----------------+ |
|                |                       | | Response Gen    | |
|                |                       | | (Google Gemini) | |
|                |                       | | - Crafts reply  | |
|                |                       | +-----------------+ |
|                |                       |                     |
|                |                       | +-----------------+ |
|                |                       | |   TTS (gTTS)    | |
|                |                       | | - Converts text | |
|                |                       | |   to audio bytes| |
|                |                       | +-----------------+ |
+----------------+                       +---------------------+


1.  **User Speaks:** The `frontend` captures audio from the user's microphone in small chunks.
2.  **Stream to Backend:** These audio chunks are streamed over a **WebSocket** connection to the `backend`.
3.  **Speech-to-Text:** The `backend` accumulates the audio chunks. Once a pause is detected or the user stops, **Whisper** transcribes the full utterance.
4.  **Emotion Detection:** The transcribed text is fed to a **fine-tuned Transformers model** to identify the user's emotion.
5.  **Response Generation:** The user's text and detected emotion are sent to the **Google Gemini Pro API**, which generates a supportive and empathetic response.
6.  **Text-to-Speech:** The generated text response is converted into audio bytes using **gTTS** and **pydub**.
7.  **Stream to Frontend:** The audio bytes of the AI's response are sent back to the `frontend` over the WebSocket.
8.  **AI Speaks:** The `frontend` plays the received audio, and the conversation continues.

## 🛠️ Technologies Used

### Backend
* **Python** (3.9+)
* **Flask:** Web framework
* **Flask-Sock:** WebSocket extension for Flask
* **Whisper (OpenAI):** Robust Speech-to-Text model
* **Hugging Face Transformers:** For custom fine-tuned emotion detection model
* **Google Gemini API:** Large Language Model for intelligent response generation
* **gTTS (Google Text-to-Speech):** Converts text to natural-sounding audio
* **Pydub:** Audio manipulation library (used for gTTS output conversion)
* **Sounddevice & SciPy:** For microphone interaction and audio file handling
* **Librosa:** Audio analysis for tone detection
* **NumPy:** Numerical operations
* **scikit-learn:** For `MultiLabelBinarizer` in emotion model

### Frontend
* **HTML5:** Structure of the web application
* **CSS3:** Styling (with custom gradients and animations)
* **JavaScript (ES6+):** Dynamic interactions, WebSockets, MediaRecorder API
* **Tailwind CSS:** Utility-first CSS framework for rapid UI development
* **Google Fonts (Inter):** Modern typography

### System Dependencies
* **FFmpeg:** Required by `pydub` for audio format conversion.

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3.9+** ([Download Python](https://www.python.org/downloads/))
* **pip** (Python package installer, usually comes with Python)
* **git** ([Download Git](https://git-scm.com/downloads/))
* **FFmpeg:**
    * **Windows:**
        1.  Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html) -> Windows icon.
        2.  Download a build (e.g., from `BtbN`).
        3.  Unzip to a simple path like `C:\ffmpeg`.
        4.  **Add `C:\ffmpeg\bin` to your System's PATH environment variable.** (Search "Environment Variables" in Windows, then "Edit the system environment variables" -> "Environment Variables..." -> Under "System variables", find "Path", click "Edit", "New", and paste `C:\ffmpeg\bin`. Click OK on all windows).
        5.  **Restart your Command Prompt/PowerShell** after changing PATH.
    * **macOS (using Homebrew):** `brew install ffmpeg`
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
    * **Verify FFmpeg:** Open a new terminal and type `ffmpeg -version`. If it shows version info, it's correctly installed.

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/conversational-emotion-recognizer.git](https://github.com/your-username/conversational-emotion-recognizer.git)
    cd conversational-emotion-recognizer
    ```
    (Replace `your-username/conversational-emotion-recognizer.git` with the actual repository URL if you host it elsewhere.)

2.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

3.  **Set up a Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *This step might take a while as it downloads large models like Whisper.*

5.  **Obtain a Google Gemini API Key:**
    * Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Generate an API Key.

6.  **Set the Gemini API Key as an Environment Variable:**
    * **IMPORTANT:** Do this in the **same terminal window** where you will run `app.py`.
    * **Windows (Command Prompt):**
        ```bash
        set GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE
        ```
    * **Windows (PowerShell):**
        ```powershell
        $env:GEMINI_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY_HERE'
        ```
    * **macOS / Linux:**
        ```bash
        export GEMINI_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY_HERE'
        ```
    *(Replace `YOUR_ACTUAL_GEMINI_API_KEY_HERE` with the key you obtained.)*

7.  **Run the Backend Server:**
    ```bash
    python app.py
    ```
    *The terminal will display messages indicating the Flask server is running (e.g., `* Running on http://127.0.0.1:5000`). Keep this terminal window open.*

8.  **Open the Frontend in your Web Browser:**
    * Navigate to the `frontend` directory in your file explorer: `conversational-emotion-recognizer/frontend/`.
    * **Double-click** on `index.html`.
    * Your default web browser will open the application.

9.  **Grant Microphone Permissions:**
    * When the page loads, your browser will prompt you for microphone access. **Click "Allow" or "Grant"** to enable voice input.

## 💬 Usage

1.  Once the frontend loads in your browser, you'll see the "AI Companion" chat interface.
2.  **Click the large microphone icon** at the bottom of the screen.
3.  **Start speaking** into your microphone.
4.  **Pause for 5 seconds or more, or click the microphone icon again** to stop recording.
5.  The system will process your speech:
    * Your transcription will appear in a purple bubble.
    * The "Emotion:" status at the top will update.
    * The AI's empathetic response will appear in a dark grey bubble, and you will hear it spoken aloud.
6.  Continue the conversation as desired!

## 📂 Project Structure

conversational-emotion-recognizer/
├── backend/
│   ├── fine_tuned_emotion_model/  # Your fine-tuned Transformers model files
│   │   ├── added_tokens.json
│   │   ├── config.json
│   │   ├── model.safetensors
│   │   └── ... (other model files)
│   ├── app.py                     # Main Flask backend application (WebSocket server)
│   ├── emotion_model.py           # Module for emotion detection using Transformers
│   ├── response_generator.py      # Module for generating AI responses using Google Gemini
│   ├── stt.py                     # Module for Speech-to-Text using Whisper and pitch detection
│   ├── requirements.txt           # List of all Python dependencies
│   ├── venv/                      # Python virtual environment (created by you)
│   └── temp_user_audio.wav        # Temporary file for user audio during processing
├── frontend/
│   ├── index.html                 # Main web page for the chat interface
│   ├── script.js                  # JavaScript for frontend logic, recording, WebSockets
│   └── style.css                  # CSS for styling the UI
└── README.md                      # This file


## 💡 Future Enhancements

* **Customizable AI Persona:** Allow users to define the AI's personality or tone.
* **Speech Emotion Recognition (SER):** Integrate audio-based emotion detection (in addition to text-based) for more nuanced understanding.
* **History Persistence:** Save conversation history and emotions.
* **Wake Word Detection:** Activate the AI by saying a specific phrase.
* **Streaming STT & TTS:** Implement truly real-time word-by-word transcription and speech generation using dedicated streaming APIs for ultra-low latency.
* **Error Handling & User Feedback:** More robust error messages and loading indicators for a smoother user experience.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/your-username/conversational-emotion-recognizer/issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
