from src.window import main_panel
from PyQt6.QtWidgets import QApplication
import ctypes
import sys

app = QApplication(sys.argv)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'apqint.pgrade.app') # workaround to get the icon on the taskbar
w = main_panel.LoginWindow()
app.exec()