import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from MainWindow import MainWindow
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()