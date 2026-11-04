from PyQt6.QtCore import QSize, QDir, QUrl, QThread
from PyQt6.QtWidgets import ( QWidget, QMainWindow, QPushButton,
                              QHBoxLayout, QFileDialog, QListView, QVBoxLayout)
from PyQt6.QtGui import QFileSystemModel, QDesktopServices
from core_classification import classify_wrapper



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ##vars
        self.folder_path = ""

        #members
        self.classifier = classify_wrapper()
        self.setWindowTitle("myapp")

        #przycisk otwierajacy widok dialogu plików
        self.path_input_button = QPushButton("Choose the folder containing the images to be processed")
        self.path_input_button.clicked.connect(self.path_input_button_clicked)

        #przycisk do przetwarzania zdjec w wybranym folderze
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_button_clicked)
        self.process_button.setEnabled(False)

        #przycisk do przeniesienia sie o katalog wyżej
        self.up_dir_button = QPushButton("Up")
        self.up_dir_button.clicked.connect(self.up_dir_button_clicked)


        #layout górnego paska
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.path_input_button)
        top_bar_layout.addWidget(self.process_button)

        self.fs_model = QFileSystemModel(self)
        self.dir_view = QListView(self)
        self.dir_view.setModel(self.fs_model)
        self.dir_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.dir_view.setViewMode(QListView.ViewMode.IconMode)
        self.dir_view.setSpacing(1)
        self.dir_view.setWordWrap(True)
        self.dir_view.setIconSize(QSize(96, 96))
        self.dir_view.setGridSize(QSize(128, 128))
        self.fs_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )
        self.fs_model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"])
        self.fs_model.setNameFilterDisables(False)
        self.dir_view.doubleClicked.connect(self.item_double_clicked)



        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.dir_view, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)
    def path_input_button_clicked(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        if self.folder_path !=  "":
            self.process_button.setEnabled(True)
            root_index = self.fs_model.setRootPath(self.folder_path)
            self.dir_view.setRootIndex(root_index)
            self.classifier.path = self.folder_path
    def process_button_clicked(self):
        self.objThread = QThread()
        self.classifier.moveToThread(self.objThread)
        self.classifier.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.classifier.run)
        self.objThread.start()
    def item_double_clicked(self, index):
        if self.fs_model.isDir(index):
            self.dir_view.setRootIndex(index)
            self.up_dir_button.setEnabled(True)


        else:
            file_path = self.fs_model.filePath(index)
            print(f"Opening image: {file_path}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
    def up_dir_button_clicked(self):
        self.dir_view.setRootIndex()