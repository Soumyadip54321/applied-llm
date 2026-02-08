'''
Script that performs STT(Speech To Text) using OPENAI's Whisper model.
This is used to convert audio recording of user's query to question which then is fed to the LLM model along with URLs to fetch
token response.
'''
import os
from functools import lru_cache
import whisper
import tempfile
from dotenv import load_dotenv
import assemblyai as aai
from langchain.agents import create_agent

load_dotenv('.env')

# fetch assembly ai API key
assemblyai_api_key = os.getenv('ASSEMBLYAI_API_KEY')

# fetch openai API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# set model to rectify transcription error such that the user query is framed correctly.
model = ChatOpenAI(
    model='gpt-5.2',
    api_key=openai_api_key,
    temperature=0.0, # higher number indicates more randomness in the model's output
    max_tokens=500, #defines the no of words in the model's response
    timeout=30 # max time in sec to wait for model's response
)

@lru_cache
def load_whisper_model():
    '''
    Function that loads Whisper model from OpenAI's Whisper model and caches it in memory.
    :return:
    '''
    return whisper.load_model('medium')

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

def fix_transcription_error(transcribed_audio : str)->str:
    '''
    Function that fixes transcription error in STT model.
    :return:
    '''
    system_prompt = f"""
                You are correcting speech-to-text errors.
                
                Rules:
                - Do NOT add new information
                - Do NOT change the meaning
                - Only fix obvious transcription mistakes
                - Preserve the original intent
                - Preserve question form if present
                
                Original transcription:
                "{transcribed_audio}"
                
                Return ONLY the corrected sentence.
                """

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt
    )

    corrected_transcription = agent.invoke({"messages":[{"role":"user","content":transcribed_audio}]})
    return corrected_transcription.content.strip()


def transcribe_audio(audio)->str:
    '''
    Function that converts audio file to text using OpenAI's Whisper model before removing the audio file stored in disc.
    :return: dictionary that contains text converted from audio.
    '''
    # get audio file path
    audio_file_path = save_audio_file(audio)

    #whisper by default assumes availability of GPU and converts audio bytes to floating point 16 numbers. In case of CPU
    # this causes issues.
    # result = whisper_model.transcribe(audio_file_path,fp16=False,language='en',
    #         task='transcribe',temperature=0.0,initial_prompt = "Indian English accent. News, economy, elections, sports etc.")

    # transcribe audio to text
    result = aai.Transcriber().transcribe(audio_file_path)

    # clean-up the temp audio file stored in disc
    os.remove(audio_file_path)

    # fix erroneous transcription
    # corrected_transcription = fix_transcription_error(result.text.strip())
    return result.text.strip()

