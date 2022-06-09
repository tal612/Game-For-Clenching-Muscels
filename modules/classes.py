import subprocess
import pygame, os, time
import csv

WIDTH = 600
HIGH = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Dino Run,main_dino_run.main,./banner photos/dino-run.png
# Doodle Jump,main_doodle_jump.main,./banner photos/doodle-jump.png 
import games.main_bubbles, games.main_doodle_jump , games.main_dino_run

class Game:
    def __init__(self, name, main_func, thumbnail) -> None:
        self.name = name
        self.thumbnail = pygame.image.load(thumbnail)
        self.thumbnail.convert()
        self.main_func = eval('games.' + main_func)


    def launch(self, threshold):
        os.chdir(self.main_path)
        subprocess.Popen(f"python main.py {threshold}", shell=True)
        # print("LAUNCHED", self.name)


class Window:
    def __init__(self, screen) -> None:
        self.current_game = None
        self.last_game = None
        self.screen = screen

    def draw_current_game(self):
        clock = pygame.time.Clock()

        img = self.current_game.thumbnail
        rect = img.get_rect()
        rect.center = -200, WIDTH / 2

        if self.last_game:
            last_img = self.last_game.thumbnail
            last_rect = last_img.get_rect()

        while rect.center[0] < HIGH / 2:
            clock.tick(120)
            time.sleep(0.001)
            self.screen.fill((255, 255, 255))

            if self.last_game:
                last_rect.center = last_rect.center[0] + 10, WIDTH / 2
                self.screen.blit(last_img, last_rect)
                pygame.draw.rect(self.screen, (255, 0, 0), last_rect, 1)

            rect.center = rect.center[0] + 8, WIDTH / 2
            self.screen.blit(img, rect)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 1)

            pygame.display.flip()

    def draw_ingame_menu(self):
        self.screen.fill(WHITE)
        pygame.display.flip()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.current_game.name, True, BLACK)

        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = HIGH / 2, 20

        self.screen.blit(text, textRect)

        pygame.display.flip()

def load_games(csv_file):
    games = []
    with open(csv_file, 'r') as db:
        reader = csv.reader(db)
        next(reader)
        for row in reader:
            games.append(Game(row[0], row[1], row[2]))
    return games

class Settings:
    def __init__(self, game) -> None:
        self.settings = {}
        self.read_set_file(game)


    def read_set_file(self,game):
        path = os.path.join( os.getcwd(), '.\settings', game + '_settings.csv' )
        with open(path, 'r') as settings_file:
            reader = csv.DictReader(settings_file)
            for row in reader:
                self.settings[row["setting"]] = row["value"]
                
if __name__ == "__main__":
    s = Settings("bubbles-shooter")
    print(s.settings)