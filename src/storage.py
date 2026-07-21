import os
import json

class DataStorage:
    def __init__(self):
        if os.name == "nt": # WIN
            self.config_dir = os.path.join(os.getenv("APPDATA"), "doccli")
        else:               # LINUX/MACOS
            self.config_dir = os.path.join(os.path.expanduser("~"), ".config", "doccli")

        # Ścieżki do plików
        self.path_mylist = os.path.join(self.config_dir, "mylist.json")
        self.path_continue = os.path.join(self.config_dir, "continue.json")
        self.path_settings = os.path.join(self.config_dir, "settings.json")
        self.path_history = os.path.join(self.config_dir, "history.json")

        # Dane
        self.mylist = []
        self.continue_data = [None, None]
        self.settings = [True, "Używa doccli!", True]
        self.history = []

        self.load()

    def load(self):
        """Wczytuje dane z dysku do zmiennych."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Moja lista
        if not os.path.exists(self.path_mylist):
            with open(self.path_mylist, 'w') as file: file.write('[]')
        with open(self.path_mylist, 'r') as file:
            self.mylist = json.load(file)

        # Kontynuuj oglądanie
        if not os.path.exists(self.path_continue):
            with open(self.path_continue, 'w') as file: json.dump([None, None], file, indent=4)
        with open(self.path_continue, 'r') as file:
            self.continue_data = json.load(file)

        # Historia
        if not os.path.exists(self.path_history):
            with open(self.path_history, 'w') as file: file.write('[]')
        with open(self.path_history, 'r') as file:
            self.history = json.load(file)

        # Ustawienia
        if not os.path.exists(self.path_settings):
            with open(self.path_settings, 'w') as file: json.dump([True, "Używa doccli!", True], file, indent=4)
        with open(self.path_settings, 'r') as file:
            self.settings = json.load(file)
            # Naprawa starych plików po aktualizacji
            if len(self.settings) != 3:
                self.settings.append(True)
                self.save()

    def save(self):
        """Zapisuje obecne zmienne na dysk."""
        with open(self.path_mylist, 'w') as file: json.dump(self.mylist, file, indent=4)
        with open(self.path_continue, 'w') as file: json.dump(self.continue_data, file, indent=4)
        with open(self.path_settings, 'w') as file: json.dump(self.settings, file, indent=4)
        with open(self.path_history, 'w') as file: json.dump(self.history, file, indent=4)

ds = DataStorage()