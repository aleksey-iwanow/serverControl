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
import cv2


base_style = """
    QPushButton{border: 3px solid green; border-radius: 20px; margin: 10px 10px; background-color: rgb(0,0,0,0)}
    QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35, 190);}
    QHeaderView::section { background-color: rgb(83,184,35); color: rgb(0,0,0); border: 2px solid rgb(0,0,0) }
    QTreeView {border: 2px solid rgb(0,0,0)}
    QLineEdit {border:3px solid rgb(83,184,35); color: rgb(83,184,35); border-radius: 20px;}

    QListWidget::item:pressed,QListWidget::item:selected{background-color:rgb(83,184,35); color: rgb(0,0,0)}
    QTableWidget::item:pressed,QTableWidget::item:selected{border:3px solid rgb(83,184,35); border-radius: 10px;color: rgb(83,184,35)}

    QTreeView::item:pressed,QTreeView::item:selected{background-color:rgb(83,184,35); color: rgb(0,0,0)}
    QTableWidget{alternate-background-color: rgba(15,15,15);}
    QWidget {
        background-color: rgb(0,0,0);
        color: #fff;
    }
    QWidget{color: rgb(83,184,35);font-size: 30px;font-family: 'CatV 6x12 9'}
"""


style_but = '''
        QPushButton{border: none; border-radius: 0px; background-color: rgb(0,0,0,0)}
        QPushButton:hover{border: none; border-radius: 0px; color: rgb(0,0,0); background-color: rgb(83,184,35);}
        '''
style_but2 = '''
        QPushButton{background-color: rgb(0,0,0,0)}
        QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35);}
        '''

style_close = """QPushButton{border: none; background-color: rgb(83,184,35,0)}
        QPushButton:hover{background-color: rgb(184,0,0); color: rgb(250,250,250); border: 0px;}"""
style_close2 = """QPushButton{color: red; border: 3px solid rgb(184,0,0); background-color: rgb(83,184,35,0); border-radius: 20px}
        QPushButton:hover{background-color: rgb(184,0,0); color: rgb(250,250,250); border: 0px;}"""
style_add = """QPushButton{color: rgb(124,99,253); border: 3px solid rgb(104,79,243); background-color: rgb(83,184,35,0); border-radius: 20px}
        QPushButton:hover{background-color: rgb(104,79,243); color: rgb(250,250,250); border: 0px;}"""


errorFormat = '<font color="red">{}</font>'
warningFormat = '<font color="orange">{}</font>'
validFormat = '<font color="green">{}</font>'
darkgreenFormat = '<font color="#80CF0C";">{}</font>'
whiteFormat = '<font color="#A1A1A1">{}</font>'
titleFormat = '<font style="color:#010101; background-color: #1F4D3C">{}</font>'
