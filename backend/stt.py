import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import librosa
import json
import numpy as np
import torch 
from emotion_model import get_emotion


try:
    print("Loading Whisper model (medium)... This might take a moment.")
  
    whisper_model = whisper.load_model("medium")
    print("Whisper model loaded.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    print("Please ensure Whisper models are downloaded and your PyTorch setup is correct (e.g., CUDA for GPU).")
    print("If error persists, try running `whisper --help` or `python -m pip install openai-whisper` for more info.")
    exit(1) 


def record_audio(filename="recorded.wav", duration=10, fs=44100):
    """Records audio from the microphone for a given duration."""
    print("🎤 Recording started...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        write(filename, fs, recording)
        print("✅ Recording saved.")
    except Exception as e:
        print(f"Error during recording: {e}")
        print("Ensure your microphone is connected and permissions are granted.")

def detect_pitch(audio_path):
    """Analyzes the average pitch (fundamental frequency) of an audio file."""
    print("🔍 Analyzing tone frequency...")
    try:
        y, sr = librosa.load(audio_path, sr=None)

        if y.size == 0 or np.mean(np.abs(y)) < 0.001:
            print("🤫 Silence or empty audio detected. No pitch.")
            return None

        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []

        for i in range(pitches.shape[1]):
            index = magnitudes[:, i].argmax()
            pitch = pitches[index, i]
            if pitch > 50: 
                pitch_values.append(pitch)

        if pitch_values:
            avg_pitch = np.mean(pitch_values)
            print(f"🎵 Detected average tone frequency: {avg_pitch:.2f} Hz")
            return avg_pitch
        else:
            print("⚠ No discernible pitch detected in the human vocal range.")
            return None
    except Exception as e:
        print(f"Error detecting pitch: {e}")
        return None

def default_converter(o):
    """Helper function to serialize NumPy types to JSON."""
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

def transcribe_audio_file(audio_path):
    """
    Transcribes a full audio file, detects pitch, and analyzes emotion.
    This is for processing the complete user utterance.
    """
    print("🧠 Transcribing final audio...")
    try:
       
        result = whisper_model.transcribe(audio_path, temperature=0, beam_size=5, fp16=torch.cuda.is_available())
        text = result["text"]
        print(f"\n📝 Transcription:\n{text}\n")

        tone = detect_pitch(audio_path)

       
        detailed, general, scores = get_emotion(text)
        print(f"\n🔍 Detected Emotions:\n→ General: {general}\n→ Detailed: {detailed}\n→ Scores: {scores}")

        return text.strip(), tone, general, detailed, scores
    except Exception as e:
        print(f"Error during final transcription or emotion detection: {e}")
        return "", None, [], [], {}

def transcribe_stream_chunk(audio_chunk_bytes):
    """Placeholder for real-time streaming ASR chunk processing."""
    return "Listening..."


if __name__ == "__main__":
  
    print("Running STT and Emotion Detection in standalone mode.")
   