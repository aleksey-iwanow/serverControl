import socket
from threading import Thread
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import subprocess
import urllib.request, urllib.error
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import datetime


class App:
    padding = -2
    x = 0

    def __init__(self):
        self.click = 0
        self.click2 = 0
        self.serial = i2c(port=1, address=0x3C)
        self.device = sh1106(self.serial, rotate=0)
        self.device.command(0xAF)
        self.width, self.height = self.device.width, self.device.height
        self.top = self.padding + 15
        self.bottom = self.height - self.padding
        self.font = ImageFont.truetype("/home/kali/CatV.ttf", 12)
        self.font2 = ImageFont.truetype("/home/kali/CatV.ttf", 15)
        self.font3 = ImageFont.truetype("/home/kali/CatV.ttf", 50)

        self.clients = []
        self.settings1 = [
            ["socket", lambda: None],
            ["server", lambda: None],
            ["reboot", self.reboot],
        ]
        self.current_menu = 0
        self.current_set = -1
        self.menus = {
            0: [self.menu1, []],
            1: [self.menu2, self.settings1],
            2: [self.menu3, []],
        }

        self.old_clicks = {
            21: 0,
            20: 0
        }
        self.active_display = True

        t = Thread(target=self.draw)
        t.start()
        t2 = Thread(target=self.upd)
        t2.start()

    def off_display(self):
        self.active_display = False
        self.device.command(0xAE)

    def on_display(self):
        self.active_display = True
        self.device.command(0xAF)

    def reboot(self):
        self.device.command(0xAE)
        subprocess.run("sudo reboot", shell=True)

    def menu1(self):
        try:
            IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        except urllib.error.URLError:
            IP = str(socket.gethostname())
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)
        cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
        temp = subprocess.check_output(cmd, shell=True)
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline=0, fill=0)
            draw.text((self.x, self.padding), "[*] Info", font=self.font2, fill=255)
            draw.text((self.x, self.top), f"IP: {str(IP)}", font=self.font, fill=255)
            draw.text((self.x, self.top + 10), str(CPU, 'utf-8'), font=self.font, fill=255)
            draw.text((self.x, self.top + 20), str(MemUsage, 'utf-8'), font=self.font, fill=255)
            draw.text((self.x, self.top + 30), str(Disk, 'utf-8'), font=self.font, fill=255)
            draw.text((self.x, self.top + 40), f"Temp: {str(temp, 'utf-8')}", font=self.font, fill=255)

    def menu3(self):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline=0, fill=0)
            d = datetime.datetime.now()
            now = f'{str(d.hour).rjust(2, "0")}:{str(d.minute).rjust(2, "0")}'
            draw.text((self.x+3, self.padding+3), now, font=self.font3, fill=255)
            """draw.text((self.x, self.padding), "[*] Users", font=self.font2, fill=255)
            i = 0
            for s in self.clients:
                if i == self.current_set:
                    draw.rectangle((self.x, self.top + i * 10, self.width + self.padding, self.top + 10 + i * 10),
                                   outline=255, fill=0)
                draw.text((self.x + 5, self.top + i * 10), f'{s.info[0]} {s.info[1]}', font=self.font, fill=23)
                i += 1"""

    def menu2(self):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline=0, fill=0)
            """cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
            temp = subprocess.check_output(cmd, shell=True)
            draw.text((self.x, self.padding), str(temp, 'utf-8'), font=self.font3, fill=255)"""
            draw.text((self.x, self.padding), "[*] Settings", font=self.font2, fill=255)
            for i in range(len(self.settings1)):
                if i == self.current_set:
                    draw.rectangle((self.x, self.top + i*10, self.width + self.padding, self.top + 10 + i*10), outline=255, fill=0)
                draw.text((self.x + 5, self.top + i*10), self.settings1[i][0], font=self.font, fill=23)

    def draw(self):
        while 1:
            self.menus[self.current_menu][0]()

    def clicked(self, clc):
        if clc == 1:
            self.current_menu = (self.current_menu - 1) % len(self.menus)
        elif clc == 2:
            self.current_set = (self.current_set - 1) % len(self.settings1)
        elif clc == 3:
            self.settings1[self.current_set][1]()
        elif clc == 4:
            self.current_set = (self.current_set + 1) % len(self.settings1)
        elif clc == 5:
            self.current_menu = (self.current_menu + 1) % len(self.menus)

    def upd(self):
        while 1:
            time.sleep(0.11)


application = App()


