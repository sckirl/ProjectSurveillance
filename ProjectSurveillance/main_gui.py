from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("MainInterface/form.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)   # load UI
        ui_file.close()

        

    def onClick():
        print("hello world")

if __name__ == "__main__":
    app = QApplication([])
    window = MainUI()
    window.ui.show()
    app.exec()