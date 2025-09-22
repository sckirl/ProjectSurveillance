from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        loadUi("form.ui", self)
        
        self.pushButton.clicked.connect(self.clickHandler)

    def clickHandler(self):
        print("hello world")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec()