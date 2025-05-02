from PySide6.QtCore import QThread, QMutex

class WorkerThread(QThread):
    """
    Worker thread class to execute a function in a separate thread.
    Optionally supports mutex locking to prevent race conditions.
    """

    def __init__(self, service_name: str, function: callable = None, args: list = None, lock_required: bool = False):
        super().__init__()
        self.service_name = service_name
        self.function = function
        self.args = args or []
        self.lock_required = lock_required
        self.mutex = QMutex()

    def run(self):
        try:
            if self.lock_required:
                self.mutex.lock()

            if self.function:
                self.function(*self.args)

        except Exception as e:
            print(f"[{self.service_name}] Error:", e)

        finally:
            if self.lock_required:
                self.mutex.unlock()

            self.cleanup()

    def cleanup(self):
        """Handles cleanup after the thread finishes."""
        print(f"[{self.service_name}] Thread finished, cleaning up.")

    def stop(self):
        """Stop the thread safely."""
        if self.isRunning():
            self.quit()
            self.wait()

