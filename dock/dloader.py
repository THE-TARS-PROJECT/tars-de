import inspect
from getpass import getuser
from PySide6.QtWidgets import QFrame
from importlib.util import spec_from_file_location, module_from_spec

class Dock:
    pass

class DLoader:
    def __init__(self):
        super(DLoader, self).__init__()

        self.docks_folder = f"/home/{getuser()}/tars/docks"
        # self.load_default()
        
    def load_default(self):
        with open(f"{self.docks_folder}/docks.txt", "r") as dock_list:
            docks_ = dock_list.read().split("\n")
            file_ = docks_[0]
            spec = spec_from_file_location(
                file_, f"{self.docks_folder}/{file_}.py"
            )
            if spec is None or spec.loader is None:
                raise ImportError("Cannot import specified dock")
            
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, QFrame) and obj.__module__ == module.__name__:
                    return obj
                else:
                    print("Cant find")

