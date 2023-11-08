import pyaudio, socket

port = 5000
ip = "127.0.0.1"

chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio().get_default_host_api_info()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)

# Create a socket connection for connecting to the server:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))

while True:
    # Recieve data from the server:
    data = client_socket.recv(1024)
    stream.write(data, chunk)
# print data

socket.close()