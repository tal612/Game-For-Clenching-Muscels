import os, csv

class Settings:
    def __init__(self, game) -> None:
        self.settings = {}
        self.read_set_file(game)

    def read_set_file(self,game):
        path = os.path.normpath(os.path.join( os.getcwd(), '.\settings', game + '_settings.csv' ))
        print('path', path)
        with open(path, 'r') as settings_file:
            reader = csv.DictReader(settings_file)
            for row in reader:
                self.settings[row["setting"]] = row["value"]
              