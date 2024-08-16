import os
from file_reader import file_reader 
from repertory import Repertory
from watchdog_handler import WatchdogHandler
from csv_manager import CSVManager


def cls():
    #fonction pour effacer la console.
    os.system('cls' if os.name == 'nt' else 'clear')


def test1(dir_name):
    print("Testing 1")
    print("---------")
    csv_manager = CSVManager()

    dossier1=Repertory(dir_name)
    dossier1.read_directory()
    print(dossier1.file_path_list)

    for file in dossier1.file_path_list:
        file=file_reader(file, csv_manager)
        file.open_file()
        print("----------")
        if file.metadata:
            print(file.metadata.name)
            print(file.metadata.created_date)
            print(file.metadata.modification_date)
            print(file.metadata.size)
        else:
            print("Les métadonnées n'ont pas été extraites.")
    print("-----------")   


if __name__ == "__main__":
    cls()   #Efface la console

    path='factures'
    csv_path = 'data/metadata.csv'  # Chemin vers votre fichier CSV
    csv_manager = CSVManager(csv_path)
    test1(path)


    watcher=WatchdogHandler(path,csv_manager)
    watcher.start()
