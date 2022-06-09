import pygame
from modules.classes import *
import serial, threading
import serial.tools.list_ports
import warnings
from modules.thread_communication import *
import sys, time

WIDTH = 600
HIGH = 800
WHITE = (255,255,255)
BLACK = (0,0,0)
global_running = True

class MainMenu:
    def __init__(self) -> None:
        self.thread_settings = ThreadSettings(True, 500)
        self.t1 = threading.Thread(target=arduino_communication, args=(pygame.K_LEFT, pygame.K_RIGHT, self.thread_settings, pygame))
        self.t1.start()

            
        self.screen = pygame.display.set_mode([HIGH, WIDTH])
        self.games = load_games("games_db.csv")
        self.running = True
        self.screen.fill((255, 255, 255))
        self.window = Window(self.screen)
        pygame.display.flip()
        self.game_index = -1
        self.ingame_menu = False
    
    def run(self):
        global global_running
                
        while self.running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.thread_settings.run = False
                    global_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game_index = (1 + self.game_index) % len(self.games)
                        self.window.current_game = self.games[self.game_index]
                        if not self.ingame_menu:
                            self.window.draw_current_game()
                            self.window.last_game = self.window.current_game
                        else:
                            self.ingame_menu = False
                            self.window.last_game = None
                            self.window.draw_current_game()
                        
                    elif event.key == pygame.K_LEFT:
                        if self.ingame_menu:
                            if self.game_index >= 0:
                                # pygame.quit()
                                self.running = False
                                self.thread_settings.run = False
                                self.t1.join()
                                self.games[self.game_index].main_func(self.thread_settings.threshold)
                        else:
                            if self.game_index >= 0:
                                self.window.draw_ingame_menu()
                                self.ingame_menu = True

            

        
        self.t1.join()
        pygame.display.quit()

def main():
    pygame.init()
    while global_running:
        main_menu = MainMenu()
        main_menu.run()
        print('ended')
    pygame.quit()

if __name__ == '__main__':
    main()
