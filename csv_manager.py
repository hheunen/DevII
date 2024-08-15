import csv
import os

class CSVManager:
    def __init__(self, csv_path='data/metadata.csv'):
        """

        Initialise une instance de CSVManager pour gérer les opérations sur un fichier CSV

        PRE:
        -`csv_path` est une chaîne représentant le chemin du fichier CSV

        POST:
        -Si le fichier CSV n'existe pas, il est créé avec les en-têtes appropriés

        """
        self.csv_path = csv_path #chemin du fichier CSV
        # Vérifie si le fichier CSV existe, sinon le crée
        if not os.path.isfile(self.csv_path):
            with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(['Pathname', 'Name', 'Created Date', 'Modification Date', 'Size'])

    def write_metadata(self, metadata):
        """Écrit une nouvelle ligne de métadonnées dans le fichier CSV."""
        with open(self.csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([
                metadata.file_path,
                metadata.name,
                metadata.created_date,
                metadata.modification_date,
                metadata.size
            ])

    def update_metadata(self, metadata):
        """
        Met à jour ou ajoute les métadonnées d'un fichier dans le CSV.

        PRE:
        -`metadata` est une instance de Metadata contenant les informations à écrire ou mettre à jour dans le CSV

        POST:
        -Le fichier CSV est mis à jour avec les nouvelles métadonnées
        -Si le fichier est trouvé, les données existantes sont mises à jour

        """

        rows = []
        updated = False
        #Lit les lignes du CSV
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            #parcours chaque ligne pour voir si le fichier existe
            for row in reader:
                if row['Pathname'] == metadata.file_path:
                    #si fichier trouvé alors met à jour les données
                    row['Name'] = metadata.name
                    row['Created Date'] = metadata.created_date
                    row['Modification Date'] = metadata.modification_date
                    row['Size'] = metadata.size
                    updated = True
                rows.append(row)

        # Réécriture du fichier CSV avec les nouvelles métadonnées mises à jour
        with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Pathname', 'Name', 'Created Date', 'Modification Date', 'Size'])
            writer.writeheader()
            writer.writerows(rows)

        if not updated:
            self.write_metadata(metadata)  # Ajoute l'entrée si elle n'existait pas

    def find_metadata(self, file_path):
        """Recherche les métadonnées d'un fichier dans le CSV."""
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Pathname'] == file_path:
                    return row
        return None
