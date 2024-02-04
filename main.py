from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from src.student import Student

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PGrade")
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()