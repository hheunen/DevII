import os
from watchdog_handler import WatchdogHandler
from csv_manager import CSVManager
from metadata import Metadata
import argparse

def reboot_csv(csv_manager, directories_to_scan):
    if os.path.exists(csv_manager.csv_path):
        try:
            os.remove(csv_manager.csv_path)
            print(f"Fichier CSV supprimé: {csv_manager.csv_path}")
        except PermissionError:
            print(f"Erreur : Le fichier '{csv_manager.csv_path}' est utilisé par un autre processus et ne peut pas être supprimé.")
            return

    csv_manager = CSVManager(csv_manager.csv_path)

    for directory in directories_to_scan:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                metadata = Metadata.from_filepath(file_path)
                metadata.save_to_csv(csv_manager)
                print(f"Metadonnees sauvegardees pour le fichier: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Gestion des métadonnées de fichiers.')
    parser.add_argument('--dir', type=str, help='Répertoire à surveiller')
    parser.add_argument('--reboot', type=str, help='Répertoire(s) pour recréer le fichier CSV')
    args = parser.parse_args()

    csv_path = 'data/metadata.csv'  # Chemin vers votre fichier CSV
    csv_manager = CSVManager(csv_path)

    if args.reboot:
        directories = args.reboot.split()
        reboot_csv(csv_manager, directories)
        print("Fichier CSV réinitialisé avec les fichiers actuels.")

    if args.dir:
        watcher = WatchdogHandler(args.dir, csv_manager)
        watcher.start()

if __name__ == "__main__":
    main()
