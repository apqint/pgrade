from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt6.QtGui import QIcon

class TaskBar(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(150, 540)
        self.setStyleSheet("background-color: black;")
        self.label = QLabel("tetx")
        self.label.move(100, 100)


class MainWindow(QMainWindow):
    def __init__(self, payload) -> None:
        super().__init__()
        self.payload = payload
        self.setWindowTitle('PGrade')
        self.setWindowIcon(QIcon('src/assets/logo.png'))
        self.setFixedSize(960, 540)
        self.setCentralWidget(TaskBar())
        self.show()
