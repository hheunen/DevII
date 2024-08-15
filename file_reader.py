from metadata import Metadata
from csv_manager import CSVManager
import os

class file_reader:

    def __init__(self, file_path, csv_manager=None):
        """
        Initialise une instance de file_reader pour lire et extraire les métadonnées d'un fichier

        PRE:
        - `file_path` est une chaîne représentant le chemin complet du fichier à lire

        POST:
        - Les attributs de l'objet file_reader sont initialisés, mais le fichier n'est pas encore ouvert
        """

        self.file_path=file_path
        self.file_state = False
        self.metadata= None
        self.file_content = None
        self.csv_manager = csv_manager or CSVManager()

    
    
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

        if not os.path.isfile(self.file_path):
            print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
            return

        try:
            with open(self.file_path, mode) as file:

                # Essaie d'ouvrir le fichier en mode lecture, si il n'y a pas d'erreur le programme passe a la ligne suivante
                #self.file = file
                # Flag pour indiquer si le fichier est ouvert ou non
                self.file_state = True
                # Méthode pour extraire les dites métadonnées (méthode définie a la ligne 30)
                self.extract_metadata()

                if self.metadata:
                    existing_metadata = self.csv_manager.find_metadata(self.file_path)
                    if existing_metadata:
                        self.metadata.update_in_csv(self.csv_manager)
                    else:
                        self.metadata.save_to_csv(self.csv_manager)

        # Gestion d'erreur    
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
        except IOError:
            print(f"Erreur : Impossible d'ouvrir le fichier '{self.file_path}'.")


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
            else:
                print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
                self.metadata = None

        else:
            print("Erreur : le fichier doit être ouvert pour extraire les métadonnées")