#Groq Whisper AI Fast Transcription App
![image](https://github.com/user-attachments/assets/3ec81466-bde9-44ec-a39b-34c1cf7bd540)
![image](https://github.com/user-attachments/assets/2133fc53-2f0d-4c3f-83ef-16f3bf51eea2)
This Streamlit-based app allows users to transcribe audio files or YouTube videos using Groq Whisper API. It provides two main functionalities:

Upload an MP3 file for transcription.
Input a YouTube URL, download the audio, and transcribe it.
Features
Audio Upload: Upload any MP3 file, re-encode it to OGG format to reduce file size, and transcribe it using the Groq Whisper API.
YouTube Audio Download: Provide a YouTube link, download the audio, re-encode it to OGG, and get a transcription.
Re-encoding: Uses ffmpeg to re-encode MP3 files to the Opus codec in OGG format, ensuring compatibility with Whisper's input limits (maximum 25MB).
Audio Embedding: After re-encoding, the audio file is embedded in the Streamlit app with a player for users to listen to the audio directly.
Technologies Used
Streamlit: Used for building the web interface.
yt-dlp: To download YouTube videos and extract audio.
pydub: Audio processing library.
ffmpeg: Used for re-encoding the audio into OGG format.This compresses the audio significantly while retaining quality suitable for transcription.
Groq Whisper API: Used for transcribing the audio.
Python: Core programming language for the app.
Prerequisites

pip install -r requirements.txt
Ensure ffmpeg is installed on your machine and available in your system's PATH.

Create a .env file in the root directory with the following contents:

GROQ_API_KEY=your_groq_api_key
Replace your_groq_api_key with your actual Groq Whisper API key.

Usage
Run the Streamlit app:

streamlit run transcript.py
The app will open in your default web browser. You can also access it at http://localhost:8501.

Transcription Options:

Tab 1 - Upload Audio: Upload an MP3 file, which will be re-encoded and then transcribed using Groq Whisper.
Tab 2 - YouTube to Audio: Enter a YouTube video URL, download the audio, and get a transcription.
Notes
The Groq Whisper API can transcribe long audio files, but re-encoding is necessary to reduce file size for optimal performance.
Ensure you have a stable internet connection, as the app interacts with the Groq API for transcription.
