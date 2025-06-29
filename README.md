# 🗣️ Conversational Emotion Recognizer (Advanced AI Companion)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-Flask--Sock-lightgrey?style=flat-square)](https://flask-sock.readthedocs.io/en/latest/)
[![Google Gemini API](https://img.shields.io/badge/Google-Gemini%20API-orange?style=flat-square&logo=google)](https://ai.google.dev/gemini-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Project Overview

The **Conversational Emotion Recognizer** is an advanced AI-powered companion designed to understand and respond to human emotions in real-time spoken conversations. By automating the analysis of sentiment and tone, this system aims to provide empathetic and contextually appropriate audio responses, enhancing human-AI interaction.

This project goes beyond simple text processing, leveraging cutting-edge AI models for robust Speech-to-Text, fine-grained Emotion Detection, intelligent Response Generation, and realistic Text-to-Speech, all delivered through a seamless web interface.

## 🚀 Key Features

* **🎙️ Real-time Speech-to-Text (STT):** Utilizes OpenAI's highly accurate Whisper model to instantly transcribe the user's spoken words into text, forming the foundation for subsequent AI processing.
* **❤️ Advanced Emotion Detection:** Employs a meticulously fine-tuned Hugging Face Transformers model to analyze the nuances of transcribed text, classifying the user's mood into distinct categories such as Happy, Sad, Surprised, Angry, Anxious, or Neutral. This enables a deeper understanding of emotional context.
* **🧠 Emotion-Aware Response Generation:** Integrates the powerful Google Gemini Pro API to dynamically craft empathetic, supportive, and contextually relevant textual replies. The AI's responses are intelligently tailored based on both the user's spoken content and the precisely detected emotional state.
* **🗣️ Natural Text-to-Speech (TTS) Output:** Converts the AI's generated textual responses back into clear, natural-sounding human speech. This is powered by Google's Text-to-Speech (gTTS) library, ensuring an auditory and engaging conversational experience for the user.
* **⚡ Seamless Real-time Interaction:** Facilitates smooth, near-instantaneous conversational turns through an efficient WebSocket-based communication channel between the web frontend and the Python backend.
* **🕒 Automatic End-of-Speech Detection:** Features an intelligent, client-side mechanism that automatically detects prolonged pauses or silence (e.g., 5 seconds of inactivity) in the user's speech, triggering the end of recording and initiation of backend processing without requiring manual intervention.
* **🌐 Intuitive Web-based Interface:** Provides a user-friendly and visually appealing chat interface accessible directly in any modern web browser, offering a familiar messaging experience for interacting with the AI companion.

## ⚙️ Architecture & How It Works

![Alt text](./photo.png)

1.  **User Speaks:** The `frontend` captures real-time audio from the user's microphone, breaking it into small, manageable chunks.
2.  **Stream to Backend:** These audio chunks are continuously streamed over a **WebSocket** connection to the `backend` server.
3.  **Speech-to-Text (STT):** The `backend` accumulates the incoming audio chunks. Upon detection of a pause (automatic or manual stop), OpenAI's **Whisper model** efficiently transcribes the complete user utterance into text.
4.  **Emotion Detection:** The transcribed text is then analyzed by a **fine-tuned Hugging Face Transformers model** to accurately identify the user's underlying emotion.
5.  **Response Generation:** Both the user's transcribed text and the detected emotional context are sent to the **Google Gemini Pro API**. Gemini intelligently generates an empathetic, supportive, and conversational text response.
6.  **Text-to-Speech (TTS):** The AI's generated text response is converted back into an audio format (WAV bytes) using **gTTS** and **pydub**, preparing it for playback.
7.  **Stream to Frontend:** The generated audio bytes of the AI's response are streamed back to the `frontend` over the same WebSocket connection.
8.  **AI Speaks:** The `frontend` receives and plays the audio, delivering the AI's response to the user, thereby completing a conversational turn.

## 🛠️ Technologies Used

| Category          | Technology/Library     | Precise Description                                                                 |
| :---------------- | :--------------------- | :---------------------------------------------------------------------------------- |
| **Backend** | Python (3.9+)          | Primary programming language for server-side logic and AI models.                   |
|                   | Flask                  | Lightweight web framework for building the RESTful API and handling requests.       |
|                   | Flask-Sock             | Extension for Flask that enables robust WebSocket communication.                    |
|                   | Whisper (OpenAI)       | State-of-the-art Speech-to-Text model for accurate audio transcription.             |
|                   | Hugging Face Transformers | Framework for building and fine-tuning the emotion detection model.             |
|                   | Google Gemini API      | Advanced Large Language Model for generating intelligent and contextual responses.  |
|                   | gTTS (Google TTS)      | Python library for converting text to natural-sounding audio using Google's TTS.    |
|                   | Pydub                  | Simple and powerful audio manipulation library, used for gTTS output conversion.    |
|                   | Sounddevice & SciPy    | Facilitate microphone interaction and efficient handling of audio data.             |
|                   | Librosa                | Audio analysis for pitch detection.                                                 |
|                   | NumPy                  | Fundamental package for numerical computing in Python.                             |
|                   | scikit-learn           | Machine learning library, used for `MultiLabelBinarizer` in emotion model setup.    |
| **Frontend** | HTML5                  | Provides the structural foundation for the web-based chat interface.                |
|                   | CSS3                   | Styles the web application, including custom gradients, animations, and responsive design. |
|                   | JavaScript (ES6+)      | Powers dynamic UI interactions, microphone access (MediaRecorder API), and WebSocket communication. |
|                   | Tailwind CSS           | A utility-first CSS framework for rapid UI development.                             |
|                   | Google Fonts (Inter)   | Ensures consistent and modern typography.                                           |
| **System Dependency** | FFmpeg                 | Essential multimedia framework required by `pydub` for audio format conversions.    |

## 🚀 Getting Started

Follow these comprehensive steps to set up and run the project locally.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3.9+** ([Download Python](https://www.python.org/downloads/))
* **pip** (Python package installer, typically bundled with Python)
* **git** ([Download Git](https://git-scm.com/downloads/))
* **FFmpeg:**
    * **Windows:**
        1.  Visit [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and click the Windows icon.
        2.  Download a pre-built executable (e.g., from `BtbN`).
        3.  Unzip the downloaded archive to a simple, easily accessible location, for example, `C:\ffmpeg`.
        4.  **Crucially, add the `bin` directory of FFmpeg to your System's PATH environment variable.** (Search for "Environment Variables" in Windows search bar -> "Edit the system environment variables" -> "Environment Variables..." -> Under "System variables", locate "Path", click "Edit", then "New", and paste the full path to your FFmpeg `bin` directory, e.g., `C:\ffmpeg\bin`. Click OK on all windows).
        5.  **Open a NEW Command Prompt/PowerShell window** after modifying the PATH for changes to take effect.
    * **macOS (using Homebrew):** `brew install ffmpeg`
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
    * **Verify FFmpeg Installation:** Open a new terminal and type `ffmpeg -version`. If it displays version information, FFmpeg is correctly installed and accessible.

### Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/vidhhya1/Conversational-Emotion-Recognizer.git
    cd emotion_detection
    ```
    

2.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

3.  **Set up a Python Virtual Environment (Highly Recommended for Isolation):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

4.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *This step will download and install all necessary Python libraries, including potentially large AI models like Whisper. It may take some time depending on your internet speed.*

5.  **Obtain a Google Gemini API Key:**
    * Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Generate a new API Key. Keep this key secure.

6.  **Set the Gemini API Key as an Environment Variable:**
    * **CRITICAL:** This variable MUST be set in the **same terminal window** where you will run `app.py`.
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
    *(**Important:** Replace `YOUR_ACTUAL_GEMINI_API_KEY_HERE` with the unique API key you obtained from Google AI Studio.)*

7.  **Run the Backend Server:**
    ```bash
    python app.py
    ```
    *The terminal will display messages indicating the Flask server is starting and running (e.g., `* Running on http://127.0.0.1:5000`). Keep this terminal window open and active.*

8.  **Open the Frontend in your Web Browser:**
    * Using your file explorer, navigate to the `frontend` directory: `conversational-emotion-recognizer/frontend/`.
    * **Double-click** on the `index.html` file.
    * Your default web browser will open the AI Companion application.

9.  **Grant Microphone Permissions:**
    * When the webpage loads, your browser will typically prompt you for permission to access your microphone. **It is essential to click "Allow" or "Grant"** for the application to be able to capture your voice input.

## 💬 Usage

1.  Once the AI Companion interface is loaded in your browser, you'll see a welcome message.
2.  **Click the prominent microphone icon** at the bottom of the chat interface. The button will likely change appearance (e.g., pulse red) to indicate recording has started.
3.  **Start speaking naturally** into your microphone.
4.  To end your turn, you have two options:
    * **Pause speaking for approximately 5 seconds:** The system will automatically detect the silence and stop recording.
    * **Click the microphone icon again:** This will manually stop the recording.
5.  After recording stops, the system will process your input:
    * Your spoken words will appear in a purple chat bubble.
    * The "Emotion:" status at the top of the interface will update to reflect the detected mood.
    * The AI's empathetic response will appear in a dark grey chat bubble, and you will hear it spoken aloud through your computer's speakers.
6.  You can then click the microphone icon again to continue the conversation!

## 📂 Project Structure

To provide a clear overview of the project's organization, here's its directory structure:
```
conversational-emotion-recognizer/
├── backend/
│   ├── fine_tuned_emotion_model/  # Directory containing your fine-tuned Hugging Face Transformers model files (e.g., config.json, model.safetensors, tokenizer files)
│   ├── app.py                     # The main Flask application, serving as the backend server and orchestrating components via WebSockets
│   ├── emotion_model.py           # Python module responsible for loading and running the emotion detection model
│   ├── response_generator.py      # Python module that interfaces with the Google Gemini API to generate AI responses
│   ├── stt.py                     # Python module handling Speech-to-Text (using Whisper) and pitch detection
│   ├── requirements.txt           # A list of all required Python dependencies for the backend
│   ├── venv/                      # (Optional, created by you) The Python virtual environment for isolated dependency management
│   └── temp_user_audio.wav        # A temporary file used to store the user's spoken audio for processing during a conversation turn
├── frontend/
│   ├── index.html                 # The primary HTML file that provides the structure of the web-based chat interface
│   ├── script.js                  # JavaScript code managing frontend logic, microphone access, WebSocket communication, and UI updates
│   └── style.css                  # CSS stylesheet defining the visual appearance and layout of the user interface
└── README.md                      # This comprehensive project documentation file
```

## 💡 Future Enhancements

* **Customizable AI Persona:** Implement features allowing users to select or define the AI's personality, tone, or specific response styles.
* **Speech Emotion Recognition (SER):** Augment the current text-based emotion detection with analysis of vocal characteristics (e.g., pitch, intonation) for a more robust and nuanced understanding of emotions.
* **Conversation History Persistence:** Add functionality to save and load past conversation transcripts and detected emotions, enabling continuity across sessions.
* **Wake Word Detection:** Integrate a wake word engine (e.g., "Hey AI") to activate the assistant without needing to click a button, for a hands-free experience.
* **Optimized Streaming STT & TTS:** Explore dedicated streaming APIs or more optimized local models for true real-time, word-by-word transcription and speech generation to minimize latency.
* **Enhanced Error Handling & User Feedback:** Implement more granular error reporting, visual loading indicators, and informative messages to improve the user experience during processing delays or issues.
* **Multi-turn Context Management:** Improve the AI's ability to remember and reference previous parts of the conversation for more coherent and natural dialogues.

## 🤝 Contributing

Contributions, issues, and feature requests are warmly welcomed! If you'd like to contribute, please feel free to check the [issues page](https://github.com/your-username/conversational-emotion-recognizer/issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
