from PySide6.QtCore import Qt
from vortexui.theme_engine import ThemeEngine
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QStackedWidget
)

from dock import dloader


class Desktop(QMainWindow):
    def __init__(self):
        super(Desktop, self).__init__()

        self.setObjectName("desktop")
        self.setAutoFillBackground(True)

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

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(9, 0, 9, 0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.mainLayout.addLayout(self.content_layout)

        """Load dock"""
        self.dloader = dloader.DLoader()
        cls, style = self.dloader.load_default()
        instance = cls()
        

        self.mainLayout.addWidget(instance)

        self.pages = QStackedWidget()
        self.mainLayout.addWidget(self.pages)
        

        self.theme_engine = ThemeEngine()
        self.setStyleSheet(
            self.theme_engine.active_scheme(
                self.theme_engine.default_theme
            )
        )
        instance.setStyleSheet(
            self.theme_engine.modify_style(style)
        )
        self.setProperty("borderColor", "none")
        
    
app = QApplication()
desktop = Desktop()
desktop.showMaximized()
app.exec()