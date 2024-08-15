import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path
        self.observer = Observer()

    def start(self):
        if not os.path.exists(self.path):
            print(f"Erreur : Le chemin '{self.path}' est introuvable.")
            return
        
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')

    def on_created(self, event):
        print(f'File {event.src_path} has been created')

    def on_deleted(self, event):
        print(f'File {event.src_path} has been deleted')



# https://www.kdnuggets.com/monitor-your-file-system-with-pythons-watchdog#:~:text=Watchdog%20is%20a%20cross%2Dplatform,changes%20with%20our%20custom%20scripts.