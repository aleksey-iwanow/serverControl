import io
import pickle
import socket
import struct
import sys
import time
from datetime import datetime
from threading import Thread
import cv2
import PIL.Image as Image
from PIL import UnidentifiedImageError, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


# 192.168.0.246  5.187.79.226 192.168.43.148
class Client:
    SERVER_HOST = "5.187.79.226"
    SERVER_PORT = 5011
    separator_token = "<SEP>"
    sz = 320*240*3

    def __init__(self):
        self.cam_port = 0
        self.cam = cv2.VideoCapture(self.cam_port)
        self.s = socket.socket()
        self.name = "none"
        self.connect()

        try:
            while True:
                print("sdsd")
                ret, frame = self.cam.read()
                if ret:
                    cv2.imwrite("image_server.png", frame)
                    im = Image.open("image_server.png")
                    im2 = im.resize((320, 240))
                    im2.save('image_server.png')
                    file = open('image_server.png', mode="rb")
                    data = file.read(self.sz)
                    self.s.sendall(data)
                    file.close()
                time.sleep(0.01)

        finally:
            self.s.close()
            sys.exit()

    def connect(self):
        try:
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.s.send('camera'.encode())
        except ConnectionRefusedError:
            self.connect()


if __name__ == '__main__':
    client = Client()
