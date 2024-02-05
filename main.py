from src.window import main_panel, second_panel
from PyQt6.QtWidgets import QApplication
import ctypes
import sys
import json

app = QApplication(sys.argv)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'apqint.pgrade.app') # workaround to get the icon on the taskbar

# this is an ugly way to check if an idnp is present
# will be rewritten later
try:
    with open("src/data.json", "r") as file:
        student_data = json.load(file)
    if student_data['code'] == 200:
        w = second_panel.MainWindow(student_data)
        app.exec()
    else:
        print("Caught else")
        w = main_panel.LoginWindow()
        app.exec()
except Exception as e:
    print(e)
    w = main_panel.LoginWindow()
    app.exec()
    with open("src/data.json") as file:
        student_data = json.load(file)
    w = second_panel.MainWindow(student_data)
    app.exec()