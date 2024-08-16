import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from datetime import datetime
from csv_manager import CSVManager
from metadata import Metadata
from file_reader import file_reader

logging.basicConfig(
    filename='application.log', 
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, path, csv_manager):
        self.path = path
        self.observer = Observer()
        self.csv_manager = CSVManager()  # Utilisation de l'instance de CSVManager

    def start(self):
        if not os.path.exists(self.path):
            logging.error(f"Erreur : Le chemin '{self.path}' est introuvable.")
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
            logging.info(f'File {event.src_path} has been modified and metadata updated')            
            print(f'File {event.src_path} has been modified and metadata updated')

    def on_created(self, event):
        if not event.is_directory:
            file = file_reader(event.src_path)
            file.open_file()
            metadata = file.metadata
            logging.info(f'File {event.src_path} has been created and metadata added')  
            print(f'File {event.src_path} has been created and metadata added')

    def on_deleted(self, event):
        if not event.is_directory:
            try:
                # Suppression des métadonnées du fichier dans le CSV
                existing_metadata = self.csv_manager.find_metadata(event.src_path)
                if existing_metadata:
                    logging.info(f'File {event.src_path} has been deleted, removing from CSV.')
                    print(f'File {event.src_path} has been deleted, removing from CSV.')
                    self.csv_manager.remove_metadata(event.src_path) 
                else:
                    logging.info(f'File {event.src_path} was deleted but not found in CSV.')
            except Exception as e:
                logging.error(f'Error processing file {event.src_path}: {str(e)}')

