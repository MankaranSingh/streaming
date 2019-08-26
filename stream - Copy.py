from flask import Flask, Response,render_template
import pyaudio
import wave
import time
from timeit import default_timer as timer

app = Flask(__name__)

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

audio1 = pyaudio.PyAudio()

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    header = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    header += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    header += bytes("WAVE",'ascii')                                              # (4byte) File type
    header += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    header += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    header += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    header += (channels).to_bytes(2,'little')                                    # (2byte)
    header += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    header += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    header += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    header += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    header += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    header += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return header

start = timer()
     
@app.route('/audio')
def audio():
    def sound():

        wf = wave.open('track.wav', 'rb')

        CHUNK = 1024
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        data = wav_header + wf.readframes(CHUNK)
        current_time = int(timer() - start)
        n_frames = int(current_time * wf.getframerate())
        wf.setpos(n_frames)
        while True:
            yield(data)
            
            data = wf.readframes(CHUNK)
        
    return Response(sound(), mimetype="audio/x-wav")

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
