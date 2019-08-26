import socket
import time
import pyaudio
import wave

audio1 = pyaudio.PyAudio()

wf = wave.open('track.wav', 'rb')

CHUNK = 1024
sampleRate = 44100
bitsPerSample = 16
channels = 2

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
while True:
    data = wf.readframes(CHUNK)
    sock.sendto(data, (MCAST_GRP, MCAST_PORT))
    time.sleep(0.0220)
