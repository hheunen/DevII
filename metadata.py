from datetime import datetime
import os


class Metadata:

    def __init__(self,name,created_date,modification_date,size):
        self.name=name
        self.created_date=created_date
        self.modification_date=modification_date
        self.size=size

    
    # ici c'est une CLASSMETHOD, cela implique que cette méthode n'est pas dépendante d'une instance de la classe.
    # On peut l'appeler sans utiliser une instance d'objet déjà créee !
    # Dans ce cas-ci cette méthode retourne un nouvelle instance de Metadata
    @classmethod
    def from_filepath(cls, file_path):
        """Crée une instance de Metadata à partir d'un chemin de fichier."""
        try:
            # Obtenir les statistiques du fichier
            file_stats = os.stat(file_path)

            # Nom du fichier
            name = os.path.basename(file_path)

            # Date de création (st_ctime peut représenter l'heure de création ou de changement d'état)
            created_date = datetime.fromtimestamp(file_stats.st_ctime)

            # Date de la dernière modification
            modification_date = datetime.fromtimestamp(file_stats.st_mtime)

            # Taille du fichier en octets
            size = file_stats.st_size

            # Retourne une instance de Metadata
            return cls(name, created_date, modification_date, size)

        except FileNotFoundError:
            print(f"Erreur : Le fichier '{file_path}' est introuvable.")
            return None