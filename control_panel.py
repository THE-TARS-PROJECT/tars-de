import re
from getpass import getuser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from thread_manager import WorkerThread
from subprocess import run, check_output
from vortexui.theme_engine import ThemeEngine
from vortexui.widgets import FSlider, FButton
from vortexui.windows import FMainWindow, FButton
from PySide6.QtWidgets import QApplication, QHBoxLayout, QGridLayout, QLabel


class ControlPanel(FMainWindow):
    def __init__(self):
        super(ControlPanel, self).__init__()

        self.setWindowTitle("Control Panel")
        self.setMinimumSize(450, 150)
        
        self.setProperty("borderColor", "default")

        print(f"Current volume: {self.get_volume()}")

        self.theme_engine = ThemeEngine()
        self.is_muted = False
        self.prev_vol = None

        self.vol_layout = QHBoxLayout()
        self.vol_btn = FButton("")
        self.vol_btn.setProperty("borderColor", "none")
        self.vol_btn.setProperty("role", "normal")
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

        self.power_text = QLabel("Power Options:")

        self.power_options_layout = QHBoxLayout()

        self.power_off_btn = FButton("Power Off", "danger")
        self.power_off_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/power.png"))

        self.logout_btn = FButton("Log Out")
        self.logout_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/logout.png"))

        self.restart_btn = FButton("Restart")
        self.restart_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/restart.png"))

        self.vol_btn.connect_func(self.on_vol_btn_clicked)
        

        self.content_layout.addLayout(self.grid_layout)

        self.content_layout.addWidget(self.power_text)
        self.content_layout.addLayout(self.power_options_layout)
        self.power_options_layout.addWidget(self.power_off_btn)
        self.power_options_layout.addWidget(self.restart_btn)
        self.power_options_layout.addWidget(self.logout_btn)
        
        btns = [self.bluetooth_btn, self.ethernet_btn]
        for index, btn in enumerate(btns):
            btn.setProperty("borderColor", "default")
            btn.update()
            btn.connect_func(self._create_thread, attach_sender=True)
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
    

    def _create_thread(self, sender):
        name = sender.text().lower()
        self.thread = WorkerThread("gnome-control-center", run, [['gnome-control-center', name]])
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_vol_btn_clicked(self):
        if not self.is_muted:
            self.prev_vol = self.get_volume()
            self.is_muted = True
            self.on_vol_change(0)
            self.vol_slider.setValue(0)
            self.vol_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/mute.png"))

        else:
            self.on_vol_change(self.prev_vol)
            self.is_muted = False
            self.vol_slider.setValue(self.prev_vol)
            self.vol_btn.setIcon(QIcon(f"/home/{getuser()}/tars/icons/volume.png"))


    def on_power_btn_clicked(self):
        run(["shutdown", "now"])


app = QApplication()
win = ControlPanel()
win.show()
app.exec()
