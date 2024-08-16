import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from datetime import datetime
from csv_manager import CSVManager
from metadata import Metadata
from file_reader import file_reader
class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, path, csv_manager):
        self.path = path
        self.observer = Observer()
        self.csv_manager = CSVManager()  # Utilisation de l'instance de CSVManager

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
        if not event.is_directory:
            file = file_reader(event.src_path)
            file.open_file()
            metadata = file.metadata            
            print(f'File {event.src_path} has been modified and metadata updated')

    def on_created(self, event):
        if not event.is_directory:
            file = file_reader(event.src_path)
            file.open_file()
            metadata = file.metadata  
            print(f'File {event.src_path} has been created and metadata added')

    def on_deleted(self, event):
        if not event.is_directory:
            file = file_reader(event.src_path)
            file.open_file()
            metadata = file.metadata  
            existing_metadata = metadata
            if existing_metadata:
                # Logic to handle deletion, for example:
                print(f'File {event.src_path} has been deleted, consider removing it from the CSV')
