"""
this is a sample file do not specify this directly
"""
from vortexui.widgets import FButton
from PySide6.QtWidgets import QFrame

class DockType:
    pass

class Dock(QFrame):
    def __init__(self):

        self.setObjectName("dock")
        
        self.setMaximumHeight(30)
        self.setMinimumHeight(30)

        # basic structure 
        # apps button in left most corner
        # time in the center
        # network controls like bluetooth, wifi ethernet on right

        self.apps_menu_btn = FButton("Menu")

