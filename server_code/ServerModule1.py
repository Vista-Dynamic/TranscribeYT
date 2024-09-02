import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import assemblyai as aai
from yt_dlp import YoutubeDL
from time import sleep
import os

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def transcribe_Anvil(url):
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'YT',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    File_URL = "YT.mp3"

    aai.settings.api_key = "d2917d44162146e086e6b6d2e96776ff"

    config = aai.TranscriptionConfig(speaker_labels=False)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        File_URL,
        config
    )

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        print(transcript.text)
        return transcript.text

    os.remove("YT.mp3")