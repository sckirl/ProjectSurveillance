from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        loadUi("form.ui", self)
        
