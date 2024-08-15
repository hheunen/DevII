import os

class Repertory:

    def __init__(self, path):
        self.path = path
        self.file_path_list = None

    # Méthode pour lire le path et obtenir la liste des path fichiers
    def read_directory(self):
        """
        Lit le répertoire spécifié par `path` et stocke la liste des fichiers dans `file_list`.
        """
        try:
            # Utilisation de os.listdir pour obtenir la liste des path des fichiers et dossiers dans le répertoire
            self.file_path_list = [os.path.join(self.path, f) for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        except FileNotFoundError:
            print(f"Erreur : Le répertoire '{self.path}' est introuvable.")
        except PermissionError:
            print(f"Erreur : Permissions insuffisantes pour lire le répertoire '{self.path}'.")
        except Exception as e:
            print(f"Une erreur inattendue est survenue : {e}")

    
