import pygame
from classes import *

WIDTH = 600
HIGH = 800
WHITE = (255,255,255)
BLACK = (0,0,0)


pygame.init()


screen = pygame.display.set_mode([HIGH, WIDTH])
games = [Game("dino-run", "./banner photos/dino-run.png", "./Dino_runGame/"),
         Game("doodle jump", "./banner photos/doodle-jump.png", "./Pygame-DoodleJump-main/"),
         Game("Bubbles Shooter", "./banner photos/Bubbles-shooter.png", "./bubbleshooter-master/")
         ]

running = True
screen.fill((255, 255, 255))
window = Window(screen)
pygame.display.flip()
game_index = -1
ingame_menu = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game_index = (1 + game_index) % len(games)
                window.current_game = games[game_index]
                if not ingame_menu:
                    window.draw_current_game()
                    window.last_game = window.current_game
                else:
                    ingame_menu = False
                    window.last_game = None
                    window.draw_current_game()
                
            elif event.key == pygame.K_LEFT:
                if ingame_menu:
                    games[game_index].launch()
                    running = False
                else:
                    window.draw_ingame_menu()
                    ingame_menu = True

    pygame.display.flip()
    
pygame.quit()