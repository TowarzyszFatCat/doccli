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
        self.history = []
        
        # Domyślne ustawienia
        self.settings = {
            "rpc_enabled": True,
            "rpc_status": "Watching anime via doccli!",
            "auto_sync": True,
            "anilist_token": "",
            "download_path": "",
            "player_quality": "best",
            "language": "pl"
        }

        self.load()

    def load(self):
        """Wczytuje dane z dysku do zmiennych i w razie potrzeby aktualizuje strukturę plików."""
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

        # Ustawienia (Z logiką migracji ze starej wersji)
        if not os.path.exists(self.path_settings):
            with open(self.path_settings, 'w') as file: json.dump(self.settings, file, indent=4)
            
        with open(self.path_settings, 'r') as file:
            loaded_settings = json.load(file)
            
            # MIGRACJA: Jeśli u kogoś na dysku ustawienia to stara lista, przerób ją na słownik
            if isinstance(loaded_settings, list):
                self.settings["rpc_enabled"] = loaded_settings[0] if len(loaded_settings) > 0 else True
                self.settings["rpc_status"] = loaded_settings[1] if len(loaded_settings) > 1 else "Używa doccli!"
                self.settings["auto_sync"] = loaded_settings[2] if len(loaded_settings) > 2 else True
                self.settings["anilist_token"] = loaded_settings[3] if len(loaded_settings) > 3 else ""
                self.settings["download_path"] = loaded_settings[4] if len(loaded_settings) > 4 else ""
                self.save() # Zapisujemy już jako słownik
                
            # Jeśli to już słownik, po prostu go ładujemy i sprawdzamy czy nie brakuje nowych kluczy
            elif isinstance(loaded_settings, dict):
                for key, default_value in self.settings.items():
                    if key not in loaded_settings:
                        loaded_settings[key] = default_value
                self.settings = loaded_settings
                self.save()

    def save(self):
        """Zapisuje obecne zmienne na dysk."""
        with open(self.path_mylist, 'w') as file: json.dump(self.mylist, file, indent=4)
        with open(self.path_continue, 'w') as file: json.dump(self.continue_data, file, indent=4)
        with open(self.path_settings, 'w') as file: json.dump(self.settings, file, indent=4)
        with open(self.path_history, 'w') as file: json.dump(self.history, file, indent=4)

ds = DataStorage()