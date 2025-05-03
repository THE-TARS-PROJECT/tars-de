import glob
from configparser import ConfigParser
from xdg.DesktopEntry import DesktopEntry

class Launcher:
    def __init__(self):
        self.apps_dir = "/usr/share/applications"

        self.apps = []
        self.__get_apps__()

    def __get_apps__(self):
        files = glob.glob(f'{self.apps_dir}/*.desktop')

        for file in files:
            entry = DesktopEntry(file)
            if not entry.getNoDisplay() and entry.getType() == "Application":
                app = {
                    "name": entry.getName(),
                    "icon": entry.getIcon(),
                    "exec": entry.getExec()
                }
                self.apps.append(app)
            else:
                pass

    def get_app(self, name: str):
        for app in self.apps:
            # print(f"app name provided - {name}, app name found - {app['name']}")
            if app['name'] == name:
                return app
