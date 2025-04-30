"""
this is a sample file do not specify this directly
"""
from PySide6.QtWidgets import QFrame

class DockType:
    pass

class Dock(QFrame):
    def __init__(self):
        
        self.setMaximumHeight(30)
        self.setMinimumHeight(30)

        self.setStyleSheet("background-color: white")

