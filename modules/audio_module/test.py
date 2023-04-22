import audio_module
import os

# Test the convert_audio function
audio_module.convert_audio('audio.mp3', 'audio.wav')

# Test the download_audio function
audio_module.download_audio('https://www.youtube.com/watch?v=_9xbnhdAOPA', 'mp3')

# Test the download_playlist function
audio_module.download_playlist('playlist.txt', 'mp3')

#clean up the the files
os.remove("audio.wav")
os.remove("Арсен Шахунц - Гудбай до свидания !.mp3")
os.remove("Гурт Made in Ukraine - Ярмарок [Concert video].mp3")
os.remove("Песня День Победы - Лев Лещенко [9 мая] HD.mp3")
