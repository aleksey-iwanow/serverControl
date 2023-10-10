import pickle
import socket
import time
from datetime import datetime
from threading import Thread
import cv2
import PIL.Image as Image
from PIL import UnidentifiedImageError, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#   5.187.79.226 192.168.43.148
class Client:
    SERVER_HOST = "5.187.79.226"
    SERVER_PORT = 5011
    separator_token = "<SEP>"
    sz = 1024 * 1024 * 10

    def __init__(self):
        self.cam_port = 0
        self.cam = cv2.VideoCapture(self.cam_port)
        self.s = socket.socket()
        self.name = "none"
        self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
        self.s.send(pickle.dumps([self.name, "command:start", datetime.now()]))
        ll = pickle.loads(self.s.recv(self.sz))
        try:
            while True:
                result, image = self.cam.read()
                print("1")
                if result:
                    # pyautogui.screenshot('image_server.png')
                    cv2.imwrite("image_server.png", image)
                    im = Image.open("image_server.png")
                    im2 = im.resize((240, 180))
                    im2.save('image_server.png')
                    file = open('image_server.png', mode="rb")

                    data = file.read(self.sz)
                    self.s.sendall(data)
                    print("jns")
                    file.close()
                    time.sleep(0.06)
        finally:
            self.s.close()


if __name__ == '__main__':
    client = Client()