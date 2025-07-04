import streamlit as st
import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import imageio_ffmpeg as ffmpeg
import yt_dlp as youtube_dl
import subprocess

# Load environment variables
load_dotenv()

# Initialize Groq API client
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

groq = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Function to convert audio to base64 for HTML playback
def audio_to_base64(file):
    try:
        with open(file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            base64_audio = base64.b64encode(audio_bytes).decode()
        return base64_audio
    except Exception as e:
        st.error(f"Error converting audio to base64: {e}")
        return None

# Function to re-encode audio to OGG using ffmpeg-python
def reencode_audio_to_ogg(input_file, output_file="encoded_audio.ogg"):
    try:
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()

        # FFmpeg command with subprocess
        command = [
            ffmpeg_path,
            "-i", input_file,             # Input file
            "-ac", "1",                   # Convert to mono
            "-c:a", "libopus",            # Use Opus codec
            "-b:a", "12k",                # 12 kbps bitrate
            "-application", "voip",       # Set application to VoIP
            output_file                   # Output file
        ]

        # Run the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            st.error(f"FFmpeg error: {result.stderr.decode()}")
            return None

        return output_file

    except Exception as e:
        st.error(f"Error re-encoding audio: {e}")
        return None

# Function to download YouTube audio
def download_youtube_audio(url, output_path="youtube_audio.mp3"):
    try:
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()  # Get the ffmpeg binary path

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'ffmpeg_location': ffmpeg_path  # Provide the ffmpeg binary path
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return output_path

    except Exception as e:
        st.error(f"Failed to download YouTube audio: {e}")
        return None

# Streamlit UI setup
st.set_page_config(layout="wide", page_title="🎤 Groq Whisper Transcription")

st.title("🎙️ Groq Whisper Transcription App")

# Tabs for Audio Upload and YouTube
tab1, tab2 = st.tabs(["📂 Upload Audio", "🎥 YouTube to Audio"])

# Tab 1: Upload and Transcribe Audio
with tab1:
    st.header("🎧 Upload MP3 for Transcription")
    uploaded_file = st.file_uploader("🔊 Upload MP3 file", type=["mp3"])

    if uploaded_file:
        with st.spinner("⚙️ Processing your audio..."):
            # Save the uploaded audio
            input_file = "uploaded_audio.mp3"
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Re-encode audio to OGG
            ogg_file = reencode_audio_to_ogg(input_file, "encoded_audio.ogg")

            if ogg_file:
                # Convert to base64 for playback
                base64_audio = audio_to_base64(ogg_file)

                # Display the audio player
                if base64_audio:
                    st.subheader("🎶 Your Uploaded Audio")
                    audio_html = f"""
                    <audio controls>
                        <source src="data:audio/ogg;base64,{base64_audio}" type="audio/ogg">
                        Your browser does not support the audio element.
                    </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)

                # Transcribe the audio
                if st.button("📝 Transcribe"):
                    with st.spinner("⏳ Transcribing your audio..."):
                        try:
                            with open(ogg_file, "rb") as audio_file:
                                transcript = groq.audio.transcriptions.create(
                                    model="whisper-large-v3",
                                    file=audio_file,
                                    response_format="text"
                                )
                            st.success("✅ Transcription complete!")
                            st.text_area("Transcription", transcript, height=300)
                        except Exception as e:
                            st.error(f"Transcription failed: {e}")
            else:
                st.error("❌ Failed to re-encode audio!")

# Tab 2: YouTube to Audio and Transcription
with tab2:
    st.header("🎥 Transcribe YouTube Video Audio")
    youtube_url = st.text_input("🔗 Enter YouTube URL")

    if st.button("⬇️ Download and Transcribe"):
        if youtube_url:
            with st.spinner("⚙️ Downloading YouTube audio..."):
                youtube_file = download_youtube_audio(youtube_url)

                if youtube_file:
                    # Re-encode YouTube audio
                    youtube_ogg_file = reencode_audio_to_ogg(youtube_file, "encoded_youtube_audio.ogg")

                    if youtube_ogg_file:
                        # Convert to base64 for HTML playback
                        base64_youtube_audio = audio_to_base64(youtube_ogg_file)

                        # Display the audio player
                        if base64_youtube_audio:
                            st.subheader("🎶 YouTube Audio")
                            youtube_audio_html = f"""
                            <audio controls>
                                <source src="data:audio/ogg;base64,{base64_youtube_audio}" type="audio/ogg">
                                Your browser does not support the audio element.
                            </audio>
                            """
                            st.markdown(youtube_audio_html, unsafe_allow_html=True)

                        # Transcribe YouTube audio
                        with st.spinner("⏳ Transcribing YouTube audio..."):
                            try:
                                with open(youtube_ogg_file, "rb") as audio_file:
                                    transcript = groq.audio.transcriptions.create(
                                        model="whisper-large-v3",
                                        file=audio_file,
                                        response_format="text"
                                    )
                                st.success("✅ Transcription complete!")
                                st.text_area("Transcription", transcript, height=300)
                            except Exception as e:
                                st.error(f"Transcription failed: {e}")
                    else:
                        st.error("❌ Failed to re-encode YouTube audio!")
                else:
                    st.error("❌ Failed to download YouTube audio!")
        else:
            st.error("❌ Please enter a valid YouTube URL")
