from audio_module import convert_audio, download_audio, download_playlist
from os import remove

# Test the convert_audio function
convert_audio('audio.mp3', 'audio.wav')

# Test the download_audio function
download_audio('https://www.youtube.com/watch?v=_9xbnhdAOPA', 'mp3')

# Test the download_playlist function
download_playlist('playlist.txt', 'mp3')

#clean up the the files
remove("audio.wav")
remove("Арсен Шахунц - Гудбай до свидания !.mp3")
remove("Гурт Made in Ukraine - Ярмарок [Concert video].mp3")
remove("Песня День Победы - Лев Лещенко [9 мая] HD.mp3")
