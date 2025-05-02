import re
from getpass import getuser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from thread_manager import WorkerThread
from subprocess import run, check_output
from vortexui.windows import FMainWindow, FButton
from vortexui.theme_engine import ThemeEngine
from vortexui.widgets import FSlider, FButton
from PySide6.QtWidgets import QApplication, QHBoxLayout, QGridLayout


class ControlPanel(FMainWindow):
    def __init__(self):
        super(ControlPanel, self).__init__()

        self.setWindowTitle("Control Panel")
        self.setMinimumSize(450, 150)
        self.setMaximumSize(400, 150)

        print(f"Current volume: {self.get_volume()}")

        self.theme_engine = ThemeEngine()

        self.vol_layout = QHBoxLayout()
        self.vol_btn = FButton("")
        self.vol_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/volume.png"))
        self.vol_slider = FSlider()
        self.vol_slider.setOrientation(Qt.Orientation.Horizontal)
        self.vol_slider.setValue(self.get_volume())

        self.vol_slider.valueChanged.connect(self.on_vol_change)

        self.content_layout.addLayout(self.vol_layout)
        self.vol_layout.addWidget(self.vol_btn)
        self.vol_layout.addWidget(self.vol_slider)

        self.grid_layout = QGridLayout()
        self.bluetooth_btn = FButton("Bluetooth")
        self.ethernet_btn = FButton("Network")

        self.power_off_btn = FButton("Power Off")
        self.power_off_btn.clicked.connect(self.on_power_btn_clicked)
        

        self.content_layout.addLayout(self.grid_layout)
        
        btns = [self.bluetooth_btn, self.ethernet_btn]
        for index, btn in enumerate(btns):
            btn.clicked.connect(self._create_thread)
            btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/{btn.text().lower()}.png"))
            self.grid_layout.addWidget(btn, 1, index)
            print(f"add: {btn.text()}")

        self.vol_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.addWidget(self.power_off_btn)
        

        self.setStyleSheet(
            self.theme_engine.active_scheme(
                self.theme_engine.default_theme
            )
        )

    def on_vol_change(self, value):
        run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"])

    def get_volume(self):
        output = check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
        match = re.search(r'(\d+)%', output)
        if match:
            return int(match.group(1))
        return None
    

    def _create_thread(self):
        name = self.sender().text().lower()
        self.thread = WorkerThread("gnome-control-center", run, [['gnome-control-center', name]])
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_power_btn_clicked(self):
        run(["shutdown", "now"])


app = QApplication()
win = ControlPanel()
win.show()
app.exec()
