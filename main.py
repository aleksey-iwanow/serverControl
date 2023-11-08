import struct
from threading import Thread
import socket
import time
import pickle
import numpy as np
from PIL import UnidentifiedImageError, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Client:
    def __init__(self, sock, cam_port=""):
        self.sock = sock
        self.cam_port = cam_port
        self.info = sock.getpeername()
        self.frame_data = b''
        self.ip, self.port = self.info
        print(self.port)


class Server:
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5011
    separator_token = "<SEP>"
    sz = 1024*1024*8 * 24

    def __init__(self):
        self.DATA = '<span style="color:green;">START CHAT</span><br><br>'
        self.client_sockets = set()
        self.audio_text = "привет"

        self.cameras = []
        self.clients = []
        self.data = b''
        self.payload_size = struct.calcsize("L")
        self.check_run = "run"
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(50)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")
        self.update_server()

    def q(self):
        for cs in self.client_sockets:
            cs.sock.close()
        self.s.close()
        quit()

    def camera(self, c):
        while True:
            conn = c.sock
            IMAGE_SIZE = 105000
            try:
                c.frame_data = b''
                while len(c.frame_data) < IMAGE_SIZE:
                    c.frame_data += conn.recv(self.sz)
                recipient = self.find_recp(c.port)
                for r in recipient:
                    print(len(c.frame_data))
                    r.sock.sendall(c.frame_data)
            except ConnectionResetError:
                self.client_sockets.remove(c)
                self.cameras.remove(c)
                c.sock.close()
                break

    def update_server(self):
        while self.check_run != "q":
            client_socket, client_address = self.s.accept()
            print(f"[+] {client_address} connected.")
            recv = client_socket.recv(1024).decode('utf-8')
            client_socket = Client(client_socket)
            self.client_sockets.add(client_socket)
            if recv == "client":
                self.clients.append(client_socket)
                t = Thread(target=self.listen, args=(client_socket,))
                t.start()
            elif recv == "camera":
                self.cameras.append(client_socket)
                t = Thread(target=self.camera, args=(client_socket,))
                t.start()
            t2 = Thread(target=self.send_, args=(client_socket,))
            t2.start()

    def find_recp(self, port):
        recps = []
        for i in self.client_sockets:
            if i.cam_port == str(port):
                recps.append(i)
                break
        return recps

    def listen(self, c):
        while True:
            msg, img = None, None
            cs = c.sock
            try:
                dtb = cs.recv(self.sz)
            except ConnectionResetError:
                self.clients.remove(c)
                self.client_sockets.remove(c)
                c.sock.close()
                break
            try:
                msg = list(pickle.loads(dtb))
            except Exception as error:
                print(error)
            sys_info = "____INFO____"
            if msg:
                spl = msg[1].split(':')
                data_list = [sys_info, "", msg[2], c.info]

                if len(spl) > 1 and spl[0] == "command":
                    if spl[1] == "start":
                        data_list[1] = self.DATA
                        cs.sendall(pickle.dumps(data_list))
                    elif spl[1] == "kill":
                        data_list[1] = "[*] Остановка сервера!"
                        cs.sendall(pickle.dumps(data_list))
                        self.q()
                    elif spl[1] == "setcam" and len(spl) > 2:
                        port = spl[2]
                        data_list[1] = f"[*] Камера {port} открыта!"
                        c.cam_port = port
                        cs.sendall(pickle.dumps(data_list))
                    elif spl[1] == "a" and len(spl) > 2:
                        print(spl[2])
                    else:
                        data_list[1] = "[*] Команда не найдена!"
                        cs.sendall(pickle.dumps(data_list))
                else:
                    data_list[1] = ": ".join(msg[:-1])
                    self.DATA += f'{data_list[1]}<br>'
                    for client_socket in self.clients:
                        client_socket.sock.send(pickle.dumps(data_list))

    def send_(self, cs):
        time.sleep(1)
        while True:
            try:
                cs.sock.send(pickle.dumps([[c.info for c in self.client_sockets]]))
                time.sleep(0.1)
            except Exception as e:
                pass


s = Server()
