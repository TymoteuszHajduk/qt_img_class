import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ##vars
        self.folder_path = ""

        self.setWindowTitle("myapp")

        #przycisk otwierajacy widok dialogu plików
        self.path_input_button = QPushButton("Choose the folder containing the images to be processed")
        self.path_input_button.clicked.connect(self.path_input_button_clicked)

        #przycisk do przetwarzania zdjec w wybranym folderze
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_button_clicked)
        self.process_button.setEnabled(False)

        layout = QHBoxLayout()
        layout.addWidget(self.path_input_button)
        layout.addWidget(self.process_button)



        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    def path_input_button_clicked(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        if self.folder_path !=  "":
            self.process_button.setEnabled(True)

    def process_button_clicked(self):
        print('fds')
