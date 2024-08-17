from metadata import Metadata
from csv_manager import CSVManager
import os
import logging

# Configuration du logger
logging.basicConfig(
    filename='application.log',  # Nom du fichier de log
    level=logging.INFO,           # Niveau de log: INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Date, type , message
)

class FileReader:

    def __init__(self, file_path, csv_manager=None):
        """
        Initialise une instance de FileReader pour lire et extraire les métadonnées d'un fichier

        PRE:
        - `file_path` est une chaîne représentant le chemin complet du fichier à lire

        POST:
        - Les attributs de l'objet FileReader sont initialisés, mais le fichier n'est pas encore ouvert
        """

        self.file_path = file_path
        self.file_state = False
        self.metadata= None
        self.file_content = None
        self.csv_manager = csv_manager or CSVManager()
        logging.info(f"Creation de FileReader pour le fichier: {file_path}")

    
    
    def open_file(self, mode='r'):
        """ 
         Ouvre le fichier spécifié en mode donné et extrait ses métadonnées

        PRE:
        - `mode` est une chaîne représentant le mode d'ouverture du fichier (par défaut 'r')

        POST:
        - Le fichier est ouvert et son état est mis à jour
        - Les métadonnées du fichier sont extraites si le fichier est ouvert avec succès
        - En cas d'erreur, un message d'erreur est affiché
        """

        try:
            with open(self.file_path, mode) as file:

                # Essaie d'ouvrir le fichier en mode lecture, si il n'y a pas d'erreur le programme passe a la ligne suivante
                self.file = file
                # Flag pour indiquer si le fichier est ouvert ou non
                self.file_state = True
                # Méthode pour extraire les dites métadonnées (méthode définie a la ligne 30)
                self.extract_metadata()

                if self.metadata:
                    existing_metadata = self.csv_manager.find_metadata(self.file_path)
                    if existing_metadata:
                        self.metadata.update_in_csv(self.csv_manager)
                        logging.info(f"Metadonnees mises a jour pour le fichier: {self.file_path}")
                    else:
                        self.metadata.save_to_csv(self.csv_manager)
                        logging.info(f"Metadonnees enregistrees pour le fichier: {self.file_path}")


        # Gestion d'erreur    
        except FileNotFoundError:
            logging.error(f"Fichier introuvable: {self.file_path}")
            print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
        except IOError:
            logging.error(f"Erreur d'ouverture du fichier: {self.file_path}")
            print(f"Erreur : Impossible d ouvrir le fichier '{self.file_path}'.")


    def extract_metadata(self):
        """
        Extrait les métadonnées du fichier ouvert

        PRE:
        - Le fichier doit être ouvert (`file_state` doit être True)

        POST:
        - Les métadonnées du fichier sont extraites et stockées dans `self.metadata`
        - Un message d'erreur est affiché si le fichier n'est pas ouvert
        """
        if self.file_state:
            if os.path.isfile(self.file_path):
                self.metadata = Metadata.from_filepath(self.file_path)
                logging.info(f"Metadonnees extraites pour le fichier: {self.file_path}")
            else:
                logging.error(f"Fichier introuvable lors de l extraction des metadonnees: {self.file_path}")
                print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
                self.metadata = None

        else:
            logging.warning("Tentative d'extraction des metadonnees sans fichier ouvert.")
            print("Erreur : le fichier doit être ouvert pour extraire les métadonnées")

def reboot_csv(csv_manager, directories_to_scan):
        if os.path.exists(csv_manager.csv_path):
            os.remove(csv_manager.csv_path)
            logging.info(f"Fichier CSV supprimé: {csv_manager.csv_path}")
    
        csv_manager = CSVManager(csv_manager.csv_path)
    
        for directory in directories_to_scan:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    metadata = Metadata.from_filepath(file_path)
                    metadata.save_to_csv(csv_manager)
                    logging.info(f"Metadonnees sauvegardees pour le fichier: {file_path}")

if __name__ == '__main__':
    directories = ['factures']
    csv_manager = CSVManager()
    reboot_csv(csv_manager, directories)
    logging.info("Fichier CSV reinitialise avec les fichiers actuels.")