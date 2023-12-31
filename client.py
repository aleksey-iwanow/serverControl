import time
from vidstream import *
import pickle
import io
import PIL.Image as Image
import numpy as np
from PIL import UnidentifiedImageError, ImageFile
from client_settings import *
import getpass
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_none(num):
    return [None for a in range(num)]


#  5.187.79.226 192.168.0.83 192.168.43.148
class Client:
    SERVER_HOST = "5.187.79.226"
    SERVER_PORT = 5011
    separator_token = "<SEP>"
    sz = 1024 * 1024 * 8 * 24

    def __init__(self, chat):
        self.chat = chat
        self.s = socket.socket()
        self.window = QLabel()
        self.window.resize(320, 240)
        self.window.show()
        self.chat.text_main = f'''<span style="color:green;">[*] Connecting to {self.SERVER_HOST}:{self.SERVER_PORT}...</span><br>'''
        self.name = str(getpass.getuser())
        try:
            self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.s.sendall("client".encode('utf-8'))
            time.sleep(0.1)
            self.s.sendall(pickle.dumps([self.name, "command:start", datetime.now()]))
            recv = pickle.loads(self.s.recv(self.sz))
            print(recv)
            self.ip, self.port = recv[3]
            print(self.ip, self.port)
            self.chat.text_main = f'''{recv[1] if len(recv) > 1 else ''}{self.chat.text_main}<span style="color:green;">[+] Connected.</span><br>'''

        except Exception as error:
            self.chat.text_main += f'''<span style="color:green;">ERROR: {error}</span><br>'''
        self.old_message = ""
        self.old_time = datetime.now()
        self.current_time = datetime.now()
        self.messages = []
        self.ts = []
        self.thr = True
        t = Thread(target=self.listen1)
        t.start()
        t1 = Thread(target=self.send)
        t1.start()

    def thread_(self, args):
        for arg in args:
            t = Thread(target=arg)
            t.start()
            self.ts.append(t)

    def set_time(self, g):
        self.old_time = g

    def listen1(self):
        while 1:
            frame_data = self.s.recv(self.sz)
            try:
                IMAGE_SIZE = 105000
                img1 = Image.open(io.BytesIO(frame_data))
                while len(frame_data) < IMAGE_SIZE:
                    frame_data += self.s.recv(self.sz)
                img = Image.open(io.BytesIO(frame_data))
                img.save(f'image1.png')
                p = QPixmap(f'image1.png').scaled(self.window.width(), self.window.height())
                self.window.setPixmap(p)
            except UnidentifiedImageError:
                try:
                    recv = frame_data
                    get = pickle.loads(recv)
                    if len(get) > 1:
                        self.old_message = get[1]
                        self.set_time(get[2])
                    else:
                        print(get)
                        self.chat.parent.tabled(get[0])
                except Exception as ex:
                    print(ex)

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
                self.old_message = f'[*] установлено имя: {self.name}'
                self.set_time(datetime.now())
            else:
                date_now = datetime.now()
                self.s.sendall(pickle.dumps([self.name, to_send, str(date_now)]))
            time.sleep(.5)


class WidgetCharacteristic(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setProperty("houdiniStyle", True)
        self.table.setIconSize(QSize(400, 500))
        self.table.setStyleSheet(
            """
            QTableWidget::item:pressed,QTableWidget::item:selected{border:3px solid rgb(104,79,243);color: rgb(104,79,243); border-radius: 10px}
            QTableWidget{border: 3px solid green; border-radius: 20px; padding: 5px 5px 5px 5px}""")
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        self.table.show()

        self.button_back = QPushButton(self.table)
        self.button_back.show()
        self.button_back.setText("Назад")
        self.button_back.resize(200, 60)

    def update_(self, ch):
        ch1 = ch["text"]
        ch2 = ch["img"]
        self.table.setRowCount(len(ch1) + len(ch2))
        self.table.setRowHeight(4, 100)
        self.table.setRowHeight(5, 300)
        index = 0

        for i in ch1:
            it = QTableWidgetItem(i)
            it.setFlags(Qt.ItemIsEnabled)
            it2 = QTableWidgetItem(ch1[i])
            it2.setForeground(QColor(104,79,243))
            self.table.setItem(index, 0, it)
            self.table.setItem(index, 1, it2)
            index += 1
        for i in ch2:
            it = QTableWidgetItem(i)
            it.setFlags(Qt.ItemIsEnabled)
            it2 = QTableWidgetItem()
            it2.setFlags(Qt.ItemIsEnabled)
            icon = QIcon(ch2[i])
            it2.setIcon(icon)
            it2.setSizeHint(QSize(100, 100))
            self.table.setItem(index, 0, it)
            self.table.setItem(index, 1, it2)
            index += 1

    def resize_event(self):
        self.table.resize(self.width() - 40, self.height() - 100)
        self.table.move(20, 20)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, self.table.width() - 320)
        self.button_back.move(0, self.table.height() - 60)


class Settings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(args[0])
        self.block1 = Block
        self.block1 = Block(self)
        self.block1.set_panels([QSettingsPanel(self.block1, "1button", "display on/off", 60),
                                QSettingsPanel(self.block1, "1button", "reboot", 60),
                                QSettingsPanel(self.block1, "default", "info", 100)])

    def res(self, size):
        self.resize(size)
        self.block1.res(QSize(size.width()-100, 200))


class Block(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(args[0])
        self.move(50, 23)
        self.panels = []
        self.setTitle('Информация')
        self.setObjectName("block1")
        self.setStyleSheet("""
            QGroupBox#block1 {
                border: 3px solid green;
                border-radius: 20px;
            }
        """)
        self.px = 10
        self.py = 30

    def set_panels(self, panels):
        self.panels = panels

    def res(self, size):
        self.resize(size.width(), 0)
        if self.panels:
            for i in range(len(self.panels)):
                p = self.panels[i]
                p.resize(self.width()-self.px*2, p.height())
                p.move(self.px, (self.panels[i - 1].y() + self.panels[i - 1].height() if i > 0 else self.py))

        self.resize(size.width(), self.panels[-1].y() + self.panels[-1].height() + self.px)


class QSettingsPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(args[0])
        self.win = args[0]
        self.text = QLabel(self)
        self.text.move(0, 0)
        self.resize(0, args[3])
        self.value = args[1]
        self.edit, self.button = get_none(2)
        if self.value == "2button":
            self.edit = QTextEdit(self)
        elif self.value == "1button":
            self.button = QPushButton(self)
        else:
            self.edit = QTextEdit(self)
        if len(args) > 2:
            self.set_text(args[2])

    def set_text(self, txt):
        self.text.setText(txt)

    def get_value(self):
        pass

    def resizeEvent(self, event):
        self.text.resize(self.width() // 2, self.height())
        if self.edit:
            self.edit.resize(self.width() // 2, self.height())
            self.edit.move(self.width() // 2, 0)
        if self.button:
            self.button.resize(self.height(), self.height())
            self.button.move(self.width() - self.height(), 0)


class AdminWidget(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(1300, 900)
        self.setStyleSheet(base_style)
        self.oldfl = None

        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start()

        self.timer2 = QTimer()
        self.timer2.setInterval(100)
        self.timer2.timeout.connect(self.timer_event2)
        self.timer2.start()

        self.widget_users = QWidget(self)
        self.widget_CHAT = MyWidget(self)
        self.widget_descript = QWidget(self)

        self.settings = Settings(self.widget_descript)

        self.widget_characteristic = WidgetCharacteristic(self)
        self.widget_characteristic.button_back.clicked.connect(self.open_window_users)

        self.table = QTableWidget(self.widget_users)  # Create a table
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["id", "IP-адрес", "порт", "Дата-подключения", "ХЗ"])
        self.table.verticalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setProperty("houdiniStyle", True)
        self.table.setStyleSheet("""QTableWidget{border: 3px solid green; border-radius: 20px; padding: 5px 5px 60px 5px}""")
        self.table.doubleClicked.connect(self.open_characteristic)
        self.users = []
        self.table.show()

        self.button_update = QPushButton(self.table)
        self.button_update.show()
        self.button_update.setText("Обновить")
        self.button_update.resize(200, 60)
        self.button_update.clicked.connect(self.update)

        self.button_characteristic = QPushButton(self.table)
        self.button_characteristic.show()
        self.button_characteristic.setText("Характеристика")
        self.button_characteristic.resize(300, 60)
        self.button_characteristic.clicked.connect(self.open_characteristic)

        self.button_delete = QPushButton(self.table)
        self.button_delete.show()
        self.button_delete.setText("Удалить")
        self.button_delete.resize(200, 60)
        self.button_delete.setStyleSheet(style_close2)
        self.button_delete.clicked.connect(self.remove_user)

        self.button_add = QPushButton(self.table)
        self.button_add.show()
        self.button_add.setText("Добавить")
        self.button_add.resize(200, 60)
        self.button_add.setStyleSheet(style_add)

        self.buttons_init()

        self.open_window_users()
        self.update()

    def timer_event(self):
        self.update()

    def timer_event2(self):
        pass

    def closeEvent(self, e):
        self.widget_CHAT.close()

    def create_user(self):
        self.admin_data.add_value(self.widget_add_user.nameEdit.text(), self.widget_add_user.passwordEdit.text())
        self.server.ftp_send("data_ad.db")
        self.open_window_users()
        self.update()

    def remove_user(self):
        row = self.table.currentRow()
        name = f'{self.table.item(row, 1)}{self.table.item(row, 2)}'
        '''self.admin_data.remove_value(row, name)
        self.server.ftp_send("data_ad.db")'''
        self.update()

    def buttons_init(self):
        self.button_users = QPushButton(self)
        self.button_chat = QPushButton(self)
        self.button_descript = QPushButton(self)
        self.button_users.setText("Пользователи")
        self.button_chat.setText("Чатик")
        self.button_descript.setText("Настройки")

        self.number_buttons = 3

        self.button_users.clicked.connect(self.open_window_users)
        self.button_chat.clicked.connect(self.open_window_chat)
        self.button_descript.clicked.connect(self.open_window_descript)
        self.buttons_menu = [self.button_users, self.button_chat, self.button_descript]
        for b in self.buttons_menu:
            b.show()

    def open_characteristic(self):
        self.update()
        index = self.table.currentRow()
        if index != -1:
            self.users[index].update_characteristic()
            self.widget_characteristic.show()
            self.widget_characteristic.update_(self.users[index].characteristic)
            self.widget_users.hide()

    def tabled(self, ls):
        try:
            self.table.show()
        except:
            return
        currentRow, currentColumn = self.table.currentRow(), self.table.currentColumn()
        ls = list(ls)
        self.table.setRowCount(len(ls))
        index = 0
        for i in ls:
            self.table.setItem(index, 0, QTableWidgetItem(str(index)))
            self.table.setItem(index, 1, QTableWidgetItem(str(i[0])))
            self.table.setItem(index, 2, QTableWidgetItem(str(i[1])))
            index += 1

        self.table.setCurrentCell(currentRow, currentColumn)

    def update(self):
        if self.isHidden():
            return
        """self.server.ftp_load("data_ad.db")
        results = self.admin_data.get_value()
        self.users.clear()
        if results:
            for i, elem in enumerate(results):
                self.users.append(User(elem[1], elem[2], elem[3], elem[4]))

        currentRow, currentColumn = self.table.currentRow(), self.table.currentColumn()

        self.table.setRowCount(len(self.users))
        index = 0
        for i in self.users:
            self.table.setItem(index, 0, QTableWidgetItem(str(index)))
            self.table.setItem(index, 1, QTableWidgetItem(i.name))
            self.table.setItem(index, 2, QTableWidgetItem(i.password))
            self.table.setItem(index, 3, QTableWidgetItem(i.date))
            if i.check == 'True':
                self.table.setItem(index, 4, QTableWidgetItem("✔"))
            else:
                self.table.setItem(index, 4, QTableWidgetItem("✘"))
            index += 1

        self.table.setCurrentCell(currentRow, currentColumn)"""

    def resizeEvent(self, e):
        w, h = self.width() // self.number_buttons, 65
        x, y = 0, 0
        step = 0
        for b in self.buttons_menu:
            b.resize(w, h)
            b.move(x + step, y)
            step += w

        self.widget_users.resize(self.width(), self.height() - h)
        self.widget_users.move(0, h)
        self.widget_CHAT.resize(self.width(), self.height() - h)
        self.widget_CHAT.move(0, h)
        self.widget_descript.resize(self.width(), self.height() - h)
        self.widget_descript.move(0, h)
        self.settings.res(self.widget_descript.size())
        self.widget_characteristic.resize(self.width(), self.height() - h)
        self.widget_characteristic.move(0, h)
        self.table.resize(self.widget_users.width() - 40, self.widget_users.height() - 40)
        self.table.move(20, 20)
        w_c = (self.table.width() - 306) // (self.table.columnCount() - 2)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, w_c)
        self.table.setColumnWidth(2, w_c)
        self.table.setColumnWidth(3, w_c)
        self.table.setColumnWidth(4, 160)

        self.button_update.move(0, self.table.height() - 60)
        self.button_characteristic.move(self.button_update.width(), self.table.height() - 60)
        self.button_delete.move(self.button_update.width() + self.button_characteristic.width(), self.table.height() - 60)
        self.button_add.move(self.button_update.width() + self.button_delete.width() + self.button_characteristic.width(), self.table.height() - 60)

        self.widget_characteristic.resize_event()

    def open_window_users(self):
        self.widget_users.show()
        self.widget_CHAT.hide()
        self.widget_descript.hide()
        self.widget_characteristic.hide()

    def open_window_chat(self):
        self.widget_users.hide()
        self.widget_CHAT.show()
        self.widget_descript.hide()
        self.widget_characteristic.hide()

    def open_window_descript(self):
        self.widget_users.hide()
        self.widget_CHAT.hide()
        self.widget_characteristic.hide()
        self.widget_descript.show()


class MyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked = False
        self.parent = args[0]
        self.text_main = ""
        self.client = Client(self)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()

        self.setMinimumSize(700, 400)
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

        self.pushButtonEnter = QPushButton(self)
        self.lineEdit = QLineEdit(self)
        self.textEdit = QTextEdit(self)

        self.label = QLabel(self)
        self.label.setStyleSheet("color: rgb(116,55,205);")

        self.pushButtonEnter.show()
        self.lineEdit.show()
        self.textEdit.show()
        self.label.show()

        self.label.move(10, 10)
        self.label.resize(1000, 31)
        self.textEdit.move(10, 40)
        self.pushButtonEnter.resize(80, 60)
        self.pushButtonEnter.setStyleSheet(style_but)

        self.lineEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: rgb(0,0,0,0)")
        self.style_ = """border: none; background: rgb(0,0,0,0); """
        self.textEdit.setStyleSheet(self.style_)
        self.textEdit.setReadOnly(True)
        self.pushButtonEnter.clicked.connect(self.clc)
        self.pushButtonEnter.setText('Esc')
        self.fl = ""
        self.fl_is_run = False
        self.function_set_txt = None
        self.label.setText(f'┌{self.client.SERVER_HOST}┐')
        self.set_text("")
        self.set_cursor()

    def resizeEvent(self, event):
        self.textEdit.resize(self.size().width() - 26, self.size().height() - 123)
        self.lineEdit.resize(self.size().width() - 88, 40)
        self.lineEdit.move(self.lineEdit.x(), self.size().height() - 73)
        self.pushButtonEnter.move(self.lineEdit.width() + 10, self.size().height() - 73)

    # слот для таймера
    def timeStep(self):
        if self.client.old_message and self.client.old_time != self.client.current_time:
            self.client.messages.append(self.client.old_message)
            self.client.current_time = self.client.old_time
            self.set_text(self.client.old_message)

    def close(self):
        self.client.thr = False
        self.client.s.close()

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
        if e.key() == Qt.Key_Escape:
            self.clc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = AdminWidget()
    client.show()
    client.setMinimumSize(QSize(900, 500))
    sys.exit(app.exec_())