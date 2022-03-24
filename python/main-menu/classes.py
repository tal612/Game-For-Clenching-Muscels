import subprocess
import pygame, os, time

WIDTH = 600
HIGH = 800
WHITE = (255,255,255)
BLACK = (0,0,0)

class Game:
    def __init__(self, name, thumbnail, main_path) -> None:
        self.name = name
        self.thumbnail = pygame.image.load(thumbnail)
        self.thumbnail.convert()
        self.main_path = main_path
    def launch(self):
        os.chdir(self.main_path)
        subprocess.Popen("python " + "main.py", shell=True)
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
         rect.center = -200,WIDTH/2

         if self.last_game:
             last_img = self.last_game.thumbnail
             last_rect = last_img.get_rect()

         while rect.center[0] < HIGH/2:
            clock.tick(120)
            time.sleep(0.001)
            self.screen.fill((255,255,255))

            if self.last_game:
                last_rect.center = last_rect.center[0] + 10, WIDTH/2
                self.screen.blit(last_img, last_rect)
                pygame.draw.rect(self.screen, (255,0,0), last_rect, 1)
               
            rect.center = rect.center[0] + 8, WIDTH/2
            self.screen.blit(img, rect)
            pygame.draw.rect(self.screen, (255,0,0), rect, 1)

            pygame.display.flip()
    
    def draw_ingame_menu(self):
        self.screen.fill(WHITE)
        pygame.display.flip()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.current_game.name, True, BLACK)

        textRect = text.get_rect()
        
        # set the center of the rectangular object.
        textRect.center =  HIGH/2, 20

        self.screen.blit(text, textRect)

        pygame.display.flip()
