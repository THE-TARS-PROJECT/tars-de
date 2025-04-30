from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QFrame
)

from dock import dloader


class Desktop(QMainWindow):
    def __init__(self):
        super(Desktop, self).__init__()

        self.setObjectName("desktop")

        # set window properties
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        """
        Layout:
        Divided in two parts
            Upper layout - for dock
            Lower layout - vertical layout (default)
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.mainLayout)

        # for test
        # self.topbar = QFrame()
        # self.topbar.setStyleSheet("background-color: white;")
        # self.topbar.setMaximumHeight(30)
        # self.topbar.setMinimumHeight(30)

        # self.text = QLabel("Hello World")
        # self.content_layout.addWidget(self.text)
        # self.mainLayout.addWidget(self.topbar)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(9, 9, 9, 9)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.mainLayout.addLayout(self.content_layout)

        """Load dock"""
        self.dloader = dloader.DLoader()
        cls = self.dloader.load_default()
        instance = cls()
        

        self.mainLayout.addWidget(instance)
        
    
app = QApplication()
desktop = Desktop()
desktop.showMaximized()
app.exec()