import socket
from threading import Thread
import pickle


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


def q():
    for cs in client_sockets:
        cs.close()

    s.close()
    quit()


def listen(cs):
    global DATA, check_run
    while True:
        try:
            msg = pickle.loads(cs.recv(1025))
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
            break
        spl = msg[1].split(':')
        data_list = [[c.getsockname() for c in client_sockets], "", msg[2]]

        if len(spl) > 1 and spl[0] == "command":
            if spl[1] == "start":
                data_list[1] = DATA
                cs.send(pickle.dumps(data_list))
            if spl[1] == "kill":
                data_list[1] = "[*] Остановка сервера!"
                cs.send(pickle.dumps(data_list))
                q()
        else:
            data_list[1] = ": ".join(msg[:-1])
            DATA += f'{data_list[1]}<br>'
            for client_socket in client_sockets:
                client_socket.send(pickle.dumps(data_list))


while check_run != "q":
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen, args=(client_socket,))
    t.start()

for cs in client_sockets:
    cs.close()

s.close()