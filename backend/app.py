import json
from flask import Flask, send_from_directory
from flask_sock import Sock
import base64
import time
import random
import os
import io 


from stt import transcribe_audio_file
from emotion_model import get_emotion
from response_generator import generate_gemini_response

from gtts import gTTS
from pydub import AudioSegment 

app = Flask(__name__, static_folder='frontend')
sock = Sock(app)

def text_to_speech(text):
    """
    Converts text to speech using Google Text-to-Speech and returns WAV bytes.
    This replaces the previous mock_text_to_speech.
    """
    print(f"TTS: Generating speech for text: '{text}' using gTTS...")
    try:
        if not text:
            text = "I have no response to generate audio for."

        tts = gTTS(text=text, lang='en', slow=False)

        mp3_io = io.BytesIO()
        tts.write_to_fp(mp3_io)
        mp3_io.seek(0)

        audio = AudioSegment.from_file(mp3_io, format="mp3")
        audio = audio.set_channels(1).set_frame_rate(16000) 

        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_bytes = wav_io.getvalue()
        print("TTS: Audio generated successfully.")
        return wav_bytes
    except Exception as e:
        print(f"Error in Text-to-Speech generation with gTTS: {e}")
        print("Ensure 'ffmpeg' is installed and accessible in your system's PATH.")
        return b'' 

@app.route('/')
def serve_index():
    """Serves the index.html file from the frontend directory."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves other static files (CSS, JS) from the frontend directory."""
    return send_from_directory(app.static_folder, filename)

@sock.route('/ws')
def chat_socket(ws):
    """Handles the WebSocket connection for real-time audio and text processing."""
    print("Client connected to WebSocket.")
    audio_buffer = io.BytesIO()

    while True:
        try:
            message = ws.receive()
            if message is None:
                break 

            if isinstance(message, str):
                data = json.loads(message)
                if data.get('event') == 'end_of_speech':
                    print("\n--- End of Speech Detected ---")

                    audio_bytes = audio_buffer.getvalue()
                    temp_audio_filename = "temp_user_audio.wav"

                    if audio_bytes:
                        with open(temp_audio_filename, "wb") as f:
                            f.write(audio_bytes)
                    else:
                        print("Warning: No audio data received for transcription.")
                        bot_response_text = "It sounds like you didn't say anything. Please try speaking into the microphone."
                        ws.send(json.dumps({
                            "type": "final_response",
                            "user_text": "No audio detected.",
                            "bot_text": bot_response_text,
                            "emotion": "Neutral",
                            "audio": base64.b64encode(text_to_speech(bot_response_text)).decode('utf-8')
                        }))
                        audio_buffer = io.BytesIO()
                        continue

            
                    final_user_text, tone_frequency, general_emotions, detailed_emotions, scores = transcribe_audio_file(temp_audio_filename)
                    os.remove(temp_audio_filename)
                    print(f"Final User Transcript: {final_user_text}")

                    
                    detected_emotion_str = ', '.join(general_emotions) if general_emotions else "Neutral"

                    
                    response_text = generate_gemini_response(
                        final_user_text,
                        general_emotions,
                        detailed_emotions,
                        tone_frequency
                    )

                    
                    response_audio_bytes = text_to_speech(response_text)
                    response_audio_b64 = base64.b64encode(response_audio_bytes).decode('utf-8')

                    final_data = {
                        "type": "final_response",
                        "user_text": final_user_text,
                        "bot_text": response_text,
                        "emotion": detected_emotion_str,
                        "audio": response_audio_b64
                    }
                    ws.send(json.dumps(final_data))

                    audio_buffer = io.BytesIO() 
                    print("Ready for next utterance.")

            elif isinstance(message, (bytearray, bytes)):
                audio_buffer.write(message)
                interim_response = {
                    "type": "interim_transcript",
                    "text": "Listening..."
                }
                ws.send(json.dumps(interim_response))

        except Exception as e:
            print(f"WebSocket Error: {e}")
            break

    print("Client disconnected from WebSocket.")

if __name__ == '__main__':
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n--- IMPORTANT ---")
        print("The GEMINI_API_KEY environment variable is NOT SET.")
        print("The AI response generator (Gemini) will NOT work correctly.")
        print("Please set it in your terminal BEFORE running app.py:")
        print("  For Windows CMD:   set GEMINI_API_KEY=YOUR_GEMINI_API_KEY")
        print("  For PowerShell:    $env:GEMINI_API_KEY='YOUR_GEMINI_API_KEY'")
        print("  For Linux/macOS:   export GEMINI_API_KEY='YOUR_GEMINI_API_KEY'")
        print("-----------------\n")

    print("Starting Flask server on http://localhost:5000")
    print("Open your frontend/index.html file in a browser to connect.")
    app.run(host='0.0.0.0', port=5000, debug=True)