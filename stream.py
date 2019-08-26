from flask import Flask, Response,render_template
import pyaudio
import wave
import struct
import time
from timeit import default_timer as timer
import socket

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

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

CHUNK = 1024
sampleRate = 44100
bitsPerSample = 16
channels = 2
wav_header = genHeader(sampleRate, bitsPerSample, channels)
     
@app.route('/audio')
def audio():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def sound():
        
        data = wav_header + sock.recv(4096)
        while data!=b'':
            yield(data)
            data = sock.recv(4096)
        
    return Response(sound(), mimetype="audio/x-wav")

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
