from docx2txt import process
from gtts import gTTS

def txt_to_audio(filename):
    text = process(filename)

    tts = gTTS(text, lang='en-us')
    tts.save('audio.mp3')
