import unittest
import csv
import os
from metadata import Metadata
from csv_manager import CSVManager
from datetime import datetime
from file_reader import FileReader
from unittest.mock import patch, MagicMock   #Créer des objets fictifs

class TestCSVManager(unittest.TestCase):

    def setUp(self):
        """Préparation de l'environnement de test."""
        self.csv_path = 'test_metadata.csv'
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        self.csv_manager = CSVManager(self.csv_path)

#Vérifie si les métadonnées sont correctement ajoutées au fichier CSV
    def test_write_metadata(self):
        """Test si les métadonnées sont correctement ajoutées au fichier CSV."""
        #Création instance Metadata
        metadata = Metadata(
            name='test_file',
            created_date='2024-08-15 09:00:00',
            modification_date='2024-08-15 09:00:00',
            size=123,
            file_path='test_file.txt'
        )
        self.csv_manager.write_metadata(metadata)

        # Lire le fichier CSV pour vérifier le contenu
        with open(self.csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Vérifier que le nombre de lignes est correct
        self.assertEqual(len(rows), 2)  # En-tête + 1 ligne de données

#Vérifie si les métadonnées existantes sont mises à jour correctement dans le fichier CSV
    def test_update_metadata(self):
        """Test la mise à jour des métadonnées dans le fichier CSV."""
        #Création de 2 instances Metadata : une pour l'ajout, l'autre pour la maj
        metadata1 = Metadata(
            name='test_file',
            created_date='2024-08-15 09:00:00',
            modification_date='2024-08-15 09:00:00',
            size=123,
            file_path='test_file.txt'
        )
        metadata2 = Metadata(
            name='test_file_updated',
            created_date='2024-08-15 10:00:00',
            modification_date='2024-08-15 10:00:00',
            size=456,
            file_path='test_file.txt'
        )
        self.csv_manager.write_metadata(metadata1)
        self.csv_manager.update_metadata(metadata2)

        # Lire le fichier CSV pour vérifier le contenu
        with open(self.csv_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Vérifier que le nombre de lignes est correct et que les données sont mises à jour
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['Name'], 'test_file_updated')
        self.assertEqual(rows[0]['Size'], '456')

class TestMetadata(unittest.TestCase):
    
    def setUp(self):
        """Prépare les données pour les tests."""
        # Crée un fichier temporaire pour les tests
        self.test_file = 'test_file.txt'
        with open(self.test_file, 'w') as f:
            f.write("Test data")

    def tearDown(self):
        """Supprime le fichier temporaire après les tests."""
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)

#Vérifie si Metadata.from_filepath() fonctionne correctement pour un fichier valide.
    def test_from_filepath_valid(self):
        """Test si `from_filepath` crée correctement une instance de Metadata."""
        metadata = Metadata.from_filepath(self.test_file)
        
        # Vérifie que les données de métadonnées sont correctes
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.name, 'test_file.txt')
        self.assertEqual(metadata.size, 9)
        self.assertEqual(metadata.created_date.date(), datetime.now().date())
        self.assertEqual(metadata.modification_date.date(), datetime.now().date())


class TestFileReader(unittest.TestCase):

    def setUp(self):
        """Préparation de l'environnement de test."""
        self.valid_file = 'test_file.txt'
        self.invalid_file = 'invalid_file.txt'
        
        # Crée un fichier temporaire pour les tests
        with open(self.valid_file, 'w') as f:
            f.write("Test data")

    def tearDown(self):
        """Nettoyage après les tests."""
        if os.path.isfile(self.valid_file):
            os.remove(self.valid_file)

#Vérifie si un fichier valide peut être ouvert et ses métadonnées extraites correctement
    def test_open_file_valid(self):
        """Test si un fichier valide peut être ouvert."""
        reader = FileReader(self.valid_file)
        reader.open_file()
        self.assertTrue(reader.file_state)
        self.assertIsInstance(reader.metadata, Metadata)
        self.assertEqual(reader.metadata.name, 'test_file.txt')

#Vérifie la gestion des erreurs lors de l'ouverture d'un fichier inexistant
    def test_open_file_invalid(self):
        """Test la gestion des erreurs lors de l'ouverture d'un fichier inexistant."""
        reader = FileReader(self.invalid_file)
        with patch('builtins.print') as mocked_print:
            reader.open_file()
            mocked_print.assert_called_with(f"Erreur : Le fichier '{self.invalid_file}' est introuvable.")
        self.assertFalse(reader.file_state)
        self.assertIsNone(reader.metadata)

#Vérifie si les métadonnées sont extraites correctement d'un fichier valide
    def test_extract_metadata_valid(self):
        """Test l'extraction des métadonnées pour un fichier valide."""
        reader = FileReader(self.valid_file)
        reader.open_file()
        reader.extract_metadata()

        self.assertIsInstance(reader.metadata, Metadata)
        self.assertEqual(reader.metadata.name, 'test_file.txt')

#Vérifie la gestion des erreurs lors de l'extraction des métadonnées d'un fichier inexistant
    def test_extract_metadata_invalid(self):
        """Test la gestion des erreurs lors de l'extraction des métadonnées d'un fichier inexistant."""
        reader = FileReader(self.invalid_file)
        reader.file_state = True  # Simule un fichier ouvert
        with patch('builtins.print') as mocked_print:
            reader.extract_metadata()
            mocked_print.assert_called_with(f"Erreur : Le fichier '{self.invalid_file}' est introuvable.")
        self.assertIsNone(reader.metadata)


if __name__ == '__main__':
    unittest.main()