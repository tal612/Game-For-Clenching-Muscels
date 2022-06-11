
import pygame
from modules.thread_communication import ThreadSettings, arduino_communication
import threading
from copy import copy

WIDTH = 800 
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
pygame.init()


class Setting:
    def __init__(self, name, func) -> None:
        self.name = name
        self.rect = None
        self.funcion = func

class SettingsApp:
    def __init__(self) -> None:
        self.thread_settings = ThreadSettings()
        self.arduino_thread = threading.Thread(target=arduino_communication,
        args=(pygame.K_LEFT, pygame.K_RIGHT, self.thread_settings, pygame,True))
        self.running = True
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        self.settings = [Setting('Set Threshold',self.threshold_setting), Setting('Exit', self.exit)]
        self.current_setting = 0

    def threshold_setting(self):
        if not self.arduino_thread.is_alive():
            return
        
        self.screen.fill(WHITE)
        pygame.display.flip()   

        done = False
        ask_set_threshold = False
        old_width, new_width = 0, 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        ask_set_threshold = False
                    elif event.key == pygame.K_LEFT:
                        if ask_set_threshold:
                            self.thread_settings.threshold = old_width
                            print("Threshold set to", new_width)
                            return

            if not ask_set_threshold:
                self.screen.fill(WHITE)
                pygame.draw.rect(self.screen, RED, pygame.Rect(WIDTH / 2 - 100, 100, 999 / 5.0, 30), 2)
                pygame.display.flip()
                old_width, new_width = 0, 0

                while new_width + 4 >= old_width:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            return
                    # print("new width =", new_width, "old width =", old_width)
                    pygame.draw.rect(self.screen, RED, pygame.Rect(WIDTH / 2 - 100, 100, new_width / 5.0, 30))
                    pygame.display.flip()
                    old_width = float(new_width)
                    new_width = float(self.thread_settings.right_voltage)
                
                ask_set_threshold = True
                font = pygame.font.Font('./modules/freesansbold.ttf', 25)
                text = font.render('Do you want to set this to the threshold? (left if yes, right if not)', True, BLACK)

                textRect = text.get_rect()
                textRect.center = WIDTH/2, 400
                self.screen.blit(text, textRect)


                pygame.display.flip() 
        


    def exit(self):
        self.running = False

    def draw_settings_list(self):
        self.screen.fill(WHITE)
        height = 70
        for setting in self.settings:
            font = pygame.font.Font('./modules/freesansbold.ttf', 32)
            text = font.render(setting.name, True, BLACK)

            textRect = text.get_rect()
            # set the center of the rectangular object.
            textRect.center = WIDTH / 2, height
            setting.rect = textRect
            self.screen.blit(text, textRect)

            

            height += 70
        
        pygame.draw.rect(self.screen, RED,self.settings[self.current_setting].rect,2)
        pygame.display.flip()
    
    def loop(self):
        self.arduino_thread.start()
        new_threshold = 500
        self.draw_settings_list()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.settings[self.current_setting].funcion()
                        self.draw_settings_list()
                    elif event.key == pygame.K_RIGHT:
                        self.current_setting = (self.current_setting + 1) % len(self.settings)
                        self.draw_settings_list()
        pygame.display.quit()
        self.thread_settings.run = False
        self.arduino_thread.join()
        return self.thread_settings.threshold

def main(threshold):
    app = SettingsApp()
    return copy(app.loop())

if __name__ == '__main__':
    main()