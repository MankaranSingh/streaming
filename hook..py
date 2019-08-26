import pyaudio
import wave
from timeit import default_timer as timer

# set desired values
start = 7
length = 3

# open wave file
wave_file = wave.open('track.wav', 'rb')

# initialize audio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=py_audio.get_format_from_width(wave_file.getsampwidth()),
                       channels=wave_file.getnchannels(),
                       rate=wave_file.getframerate(),
                       output=True)

# skip unwanted frames
n_frames = int(start * wave_file.getframerate())
wave_file.setpos(n_frames)

# write desired frames to audio buffer
n_frames = int(length * wave_file.getframerate())
frames = wave_file.readframes(n_frames)
start = timer()
stream.write(frames)
end = timer()
print(end - start)

# close and terminate everything properly
stream.close()
py_audio.terminate()
wave_file.close()
