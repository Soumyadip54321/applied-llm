'''
Script that performs STT(Speech To Text) using ASSEMBLYAI model.
This is used to convert audio recording of user's query to question which then is fed to the LLM model along with URLs to fetch
token response.
'''
import os
import time
from functools import lru_cache
import whisper
import tempfile
from dotenv import load_dotenv
import assemblyai as aai
from langchain.agents import create_agent

load_dotenv('.env')

# fetch assemblyAI & OPENAI API key
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

@lru_cache
def load_whisper_model():
    '''
    Function that loads 'base' WHISPER model from disk to be used as a failsafe option in case AssemblyAI fails to transcribe audio.
    :return:
    '''
    return whisper.load_model('base')

def save_audio_file(audio):
    '''
    Function that saves audio file to disk in a temporary file. Whisper expects input audio to not be in bytes but as a file
    path such as file.mp3/file.wav etc.
    :param audio: Audio bytes fetched from frontend stored in RAM.
    :return:
    '''
    # Whisper requires the audio file to exist so long it doesn't convert audio bytes to text hence we set delete=False below.
    with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as f:
        # writes entire audio byte like data from buffer in RAM to .wav file
        f.write(audio.getbuffer())
        # output file path to .wav
        return f.name

def transcribe_audio(audio)->str:
    '''
    Function that uses AssemblyAI model which if fails uses Whisper model to convert audio containing user question to text.
    :return: text captured from audio.
    '''
    # get audio file path
    audio_file_path = save_audio_file(audio)

    # transcribe audio to text using universal-2 model
    config = aai.TranscriptionConfig(
        speech_models=["universal-2"]  # or "universal-3-pro"
    )

    # Assembly AI creates a job to transcribe the audio file with status=queued.
    result = aai.Transcriber(config=config).transcribe(audio_file_path)

    # since transcription is asynchronous in nature we wait for sometime before fetching the job to check whether it got completed or errored out
    while result.status not in ["completed", "error"]:
        # wait 1 sec prior to fetching job
        time.sleep(1)
        # fetch updated job which's assumed to contain the converted text from audio & status
        result = transcriber.get_transcript(result.id)

    # if job errored out use whisper model to transcribe audio.
    if result.status == "error":
        whisper_model = load_whisper_model()
        result = whisper_model.transcribe(audio_file_path,language="en")

    # clean-up the temp audio file stored in disc
    os.remove(audio_file_path)

    return result.text.strip()

