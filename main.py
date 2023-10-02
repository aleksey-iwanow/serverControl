import socket
import time
from threading import Thread
import pickle
import io
import PIL.Image as Image
from PIL import UnidentifiedImageError, ImageFile


class Client:
    def __init__(self, sock, cam_ip=""):
        self.sock = sock
        self.cam_ip = cam_ip
        self.info = sock.getpeername()
        print(self.info)
        self.ip, self.port = self.info


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5011
DATA = '<span style="color:green;">START CHAT</span><br><br>'
separator_token = "<SEP>"
client_sockets = set()
check_run = "run"
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(50)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
sz = 1024*1024*10


def q():
    for cs.sock in client_sockets:
        cs.sock.close()

    s.close()
    quit()


def find_recp(ip):
    recps = []
    for i in client_sockets:
        if i.cam_ip == ip:
            recps.append(i)
    return recps


def listen(c):
    global DATA, check_run
    while True:
        msg, img = None, None
        cs = c.sock
        try:
            dtb = cs.recv(sz)
            try:
                img = Image.open(io.BytesIO(dtb))
                img = dtb
            except UnidentifiedImageError:
                msg = pickle.loads(dtb)
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(c)
            break
        sys_info = "____INFO____"
        if msg:
            spl = msg[1].split(':')
            data_list = [sys_info, "", msg[2]]

            if len(spl) > 1 and spl[0] == "command":
                if spl[1] == "start":
                    data_list[1] = DATA
                    cs.send(pickle.dumps(data_list))
                elif spl[1] == "kill":
                    data_list[1] = "[*] Остановка сервера!"
                    cs.send(pickle.dumps(data_list))
                    q()
                elif spl[1] == "setcam" and len(spl) > 2:
                    ip = spl[2]
                    data_list[1] = f"[*] Камера {ip} открыта!"
                    c.cam_ip = ip
                    cs.send(pickle.dumps(data_list))
                else:
                    data_list[1] = "[*] Команда не найдена!"
                    cs.send(pickle.dumps(data_list))
            else:
                data_list[1] = ": ".join(msg[:-1])
                DATA += f'{data_list[1]}<br>'
                for client_socket in client_sockets:
                    client_socket.sock.send(pickle.dumps(data_list))
        elif img:
            recipient = find_recp(c.ip)
            for r in recipient:
                r.sock.sendall(img)


def send(cs):
    while True:
        try:
            cs.sock.send(pickle.dumps([[c.info for c in client_sockets]]))
            time.sleep(.5)
        except Exception as e:
            pass


while check_run != "q":
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_socket = Client(client_socket)
    client_sockets.add(client_socket)
    t = Thread(target=listen, args=(client_socket,))
    t.start()
    t2 = Thread(target=send, args=(client_socket,))
    t2.start()

for cs in client_sockets:
    cs.close()

s.close()