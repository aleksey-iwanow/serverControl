import time

from client_settings import *


# 5.187.79.226 192.168.0.246
class Client:
    SERVER_HOST = "5.187.79.226"
    SERVER_PORT = 5011
    separator_token = "<SEP>"

    def __init__(self, chat):
        self.chat = chat
        self.s = socket.socket()
        self.chat.text_main = f'''<span style="color:green;">[*] Connecting to {self.SERVER_HOST}:{self.SERVER_PORT}...</span><br>'''
        try:
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.s.send("command:start".encode())
            self.chat.text_main = f'''{self.s.recv(1024).decode()}{self.chat.text_main}<span style="color:green;">[+] Connected.<br>Enter your name: </span><br>'''

        except Exception as error:
            self.chat.text_main += f'''<span style="color:green;">ERROR: {error}</span><br>'''
        self.name = "none"
        self.old_message = ""
        self.current_message = ""
        self.messages = []
        self.ts = []
        self.thr = True
        self.thread_([self.send, self.listen])

    def thread_(self, args):
        for arg in args:
            t = Thread(target=arg)
            t.start()
            self.ts.append(t)

    def listen(self):
        while self.thr:
            message = self.s.recv(1024).decode()
            self.old_message = message

    def send(self):
        while self.thr:
            if not self.chat.clicked:
                continue
            self.chat.clicked = False
            to_send = self.chat.lineEdit.text()
            if to_send.lower() == 'q':
                break
            if self.name == "none":
                self.name = to_send
                self.old_message = f'установлено имя: {self.name}'
            else:
                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                to_send = f"[{date_now}] {self.name}{self.separator_token}{to_send}"
                self.s.send(to_send.encode())
            time.sleep(1)


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('textRedactor.ui', self)
        self.clicked = False
        self.text_main = ""
        self.client = Client(self)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()

        self.setMinimumSize(700, 400)
        self.lineEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.textEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.setObjectName("app")
        self.setStyleSheet("""
            QLabel#app {
                background-color: rgb(0,0,0,220);

                border: 4px solid rgb(83,184,35);
                outline: 5px solid darkblue;
                color: #fff;
            }
            QWidget{color: rgb(83,184,35);font-size: 30px;font-family: 'CatV 6x12 9'; background-color: rgb(0,0,0,0);}
        """)

        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton.hide()
        self.pushButtonEnter.clicked.connect(self.clc)
        self.pushButtonEnter.setStyleSheet(style_but)
        self.fl = ""
        self.fl_is_run = False
        self.function_set_txt = None
        self.label.setText(f'┌{os.getcwd()}┐')
        self.set_text("")
        self.set_cursor()

    def resizeEvent(self, event):
        self.textEdit.resize(self.size().width() - 26, self.size().height() - 123)
        self.lineEdit.resize(self.size().width() - 88, 40)
        self.lineEdit.move(self.lineEdit.x(), self.size().height() - 73)
        self.pushButton_4.move(10, self.size().height() - 80)
        self.pushButton_3.move(120, self.size().height() - 80)
        self.pushButton_2.move(230, self.size().height() - 80)
        self.pushButton.move(340, self.size().height() - 80)
        self.pushButtonEnter.move(self.lineEdit.width() + 10, self.size().height() - 73)

    # слот для таймера
    def timeStep(self):
        if self.client.old_message and self.client.old_message != self.client.current_message:
            self.client.messages.append(self.client.old_message)
            self.client.current_message = self.client.old_message
            self.set_text(self.client.old_message)

    def closeEvent(self, e):
        self.client.thr = False
        self.client.s.close()
        app.quit()

    def set_text(self, text):
        self.textEdit.setText(
            f'''<div>{self.text_main}{text}</div>''')
        self.text_main = self.textEdit.toHtml()
        self.set_cursor()

    def set_cursor(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def clc(self):
        self.clicked = True

    def keyPressEvent(self, e):
        count = len(self.textEdit.toPlainText().split("\n"))
        self.label_2.setText(f'┌{count}┐')
        if e.key() == Qt.Key_Escape:
            self.clc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = MyWidget()
    client.show()
    client.setMinimumSize(QSize(600, 400))
    sys.exit(app.exec_())