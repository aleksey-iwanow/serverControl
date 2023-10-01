import socket
import random
from threading import Thread
from datetime import datetime
import platform, socket, re, uuid, json, psutil, logging
import os
from PyQt5.QtWidgets import QGraphicsColorizeEffect
import subprocess as sp
import sys
from datetime import datetime
import subprocess
from os import listdir, path, getcwd
from PIL import Image
from PyQt5 import uic, QtGui  # Импортируем uic
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, QTimer, QRect
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QWidget, QFileDialog, \
    QGraphicsOpacityEffect, QLabel, QTextEdit, QLineEdit, QPushButton, QFrame
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from textRedactor import Ui_MainWindow


style_but = '''
        QPushButton{background-color: rgb(0,0,0,0)}
        QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35);}
        '''
style_but2 = '''
        QPushButton{background-color: rgb(0,0,0,0)}
        QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35);}
        '''

errorFormat = '<font color="red">{}</font>'
warningFormat = '<font color="orange">{}</font>'
validFormat = '<font color="green">{}</font>'
darkgreenFormat = '<font color="#80CF0C";">{}</font>'
whiteFormat = '<font color="#A1A1A1">{}</font>'
titleFormat = '<font style="color:#010101; background-color: #1F4D3C">{}</font>'


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()