import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
import argparse
import cmd
from datetime import datetime
from csv_manager import CSVManager
from metadata import Metadata
from file_reader import FileReader

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
        print(f"Surveillance du répertoire '{self.path}' démarrée.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def on_modified(self, event):
        if not event.is_directory:
            file = FileReader(event.src_path)
            file.open_file()
            metadata = file.metadata
            logging.info(f'File {event.src_path} has been modified and metadata updated')            
            print(f'File {event.src_path} has been modified and metadata updated')

    def on_created(self, event):
        if not event.is_directory:
            file = FileReader(event.src_path)
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

def reboot_csv(csv_manager, directories_to_scan):
    if os.path.exists(csv_manager.csv_path):
        try:
            os.remove(csv_manager.csv_path)
            logging.info(f"Fichier CSV supprimé: {csv_manager.csv_path}")
        except PermissionError:
            logging.error(f"Le fichier {csv_manager.csv_path} est utilisé par un autre processus et ne peut pas être supprimé.")
            print(f"Erreur : Le fichier '{csv_manager.csv_path}' est utilisé par un autre processus et ne peut pas être supprimé.")
            return

    csv_manager = CSVManager(csv_manager.csv_path)

    for directory in directories_to_scan:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                metadata = Metadata.from_filepath(file_path)
                metadata.save_to_csv(csv_manager)
                logging.info(f"Metadonnees sauvegardees pour le fichier: {file_path}")

class FileMonitorShell(cmd.Cmd):
    intro = 'Bienvenue dans l\'interface de commande de gestion de fichiers. Tapez help ou ? pour l\'aide.'
    prompt = '(file-monitor) '

    def __init__(self, csv_manager):
        super().__init__()
        self.csv_manager = csv_manager
        self.handler = None

    def do_start(self, path):
        """Commence à surveiller les fichiers dans le répertoire donné."""
        if not path:
            print('Vous devez spécifier un chemin.')
            return

        if not os.path.exists(path):
            print(f"Le chemin '{path}' n'existe pas.")
            return

        if self.handler:
            self.handler.observer.stop()
        self.handler = WatchdogHandler(path, self.csv_manager)
        self.handler.start()

    def do_reboot(self, directories):
        """Recrée le fichier CSV avec les métadonnées des fichiers dans les répertoires spécifiés."""
        directories = directories.split()
        reboot_csv(self.csv_manager, directories)

    def do_exit(self, line):
        """Quitte l'interface de commande."""
        if self.handler:
            self.handler.observer.stop()
        print('Merci d\'avoir utilisé l\'interface de commande.')
        return True
