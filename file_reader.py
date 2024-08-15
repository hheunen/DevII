from metadata import Metadata

class file_reader:

    def __init__(self, file_path):

        self.file_path=file_path
        self.file_state = False
        self.metadata= None
        self.file_content = None

    
    
    def open_file(self, mode='r'):

        try:
            # Essaie d'ouvrir le fichier en mode lecture, si il n'y a pas d'erreur le programme passe a la ligne suivante
            self.file = open(self.file_path, mode) 
            # Flag pour indiquer si le fichier est ouvert ou non
            self.file_state = True
            # Méthode pour extraire les dites métadonnées (méthode définie a la ligne 30)
            self.extract_metadata()

        # Gestion d'erreur    
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.file_path}' est introuvable.")
        except IOError:
            print(f"Erreur : Impossible d'ouvrir le fichier '{self.file_path}'.")


    def extract_metadata(self):
        if self.file_state:
            self.metadata = Metadata.from_filepath(self.file_path)
        else:
            print("Erreur : le fichier doit être ouvert pour extraire les métadonnées")