from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QApplication
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QDoubleValidator, QIcon
from ..student import Student
import json
class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 540)
        self.setWindowTitle("PGrade")   
        self.setWindowIcon(QIcon("src/assets/logo.png"))
        font_id = QFontDatabase.addApplicationFont("src/assets/font.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        background = QLabel(self)
        background.resize(960, 540)
        pixmap = QPixmap('src/assets/background.png')
        background.setPixmap(pixmap)

        login_label = QLabel("Login", self)
        login_label.resize(200,200)
        login_label.setFont(QFont(families[0], 40))
        login_label.move(415, 180)
        login_label.setStyleSheet("color: white;")

        self.idnp_input = QLineEdit(self)
        self.idnp_input.setValidator(QDoubleValidator())
        self.idnp_input.resize(220, 40)
        self.idnp_input.move(370, 330)
        self.idnp_input.setMaxLength(13)
        self.idnp_input.setStyleSheet('color:white; background-color: rgba(0,0,0,0); font-size:28px; border: null; border-bottom: 3px solid rgba(35, 17, 35, 0.8); color:white;') # border-radius: 5px; border-top-left-radius: 7px; border-top-right-radius: 7px;
        self.idnp_input.setPlaceholderText('IDNP:') # 8 spaces to center
        self.idnp_input.textChanged.connect(self.onTextChanged)
        self.idnp_input.returnPressed.connect(self.processID)
        
        self.button = QPushButton(self)
        self.button.setText("Start")
        self.button.resize(220, 40)
        self.button.move(370, 385)
        self.button.setStyleSheet("color:gray; font-size: 25px; background-color: #372554; border-radius: 5px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px;")
        self.button.clicked.connect(self.changeColorThenProcessID)
        self.show()

    def changeColorThenProcessID(self):
        self.button.setStyleSheet(f"color: white; font-size: 25px; border-radius: 5px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; background-color: #372554")
        self.processID()

    def processID(self):
        idnp = self.idnp_input.text()
        if len(idnp)==13:
            self.idnp_input.setReadOnly(True)
            self.idnp_input.selectionChanged.connect(lambda: self.idnp_input.setSelection(0, 0))
            self.button.setDisabled(True)
            student = Student(idnp)
            self.button.setText('Loading...')
            self.button.setStyleSheet("color:gray; font-size: 25px; background-color: #372554; border-radius: 5px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px;")
            QApplication.processEvents()
            student.getData()
            self.button.setText('Start')
            self.button.setDisabled(False)
            self.idnp_input.setReadOnly(False)
            self.idnp_input.setText('')
            self.idnp_input.setPlaceholderText('    Invalid IDNP')
            self.button.setStyleSheet("color: gray; font-size: 25px; background-color: #372554; border-radius: 5px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px;")
            if student.payload['code']==200:
                with open("src/data.json", "w+") as file:
                    json.dump(student.payload, file, indent=4)
                self.close()
                

    def onTextChanged(self):
        self.button.setStyleSheet(f"{'color:white;' if len(self.idnp_input.text())==13 else 'color:gray;'} font-size: 25px; border-radius: 5px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; background-color: #{'52528C' if len(self.idnp_input.text())==13 else '372554'}")
    
        


