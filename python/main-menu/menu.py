import subprocess
import pygame, os

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

WIDTH = 600
HIGH = 800

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([HIGH, WIDTH])
games = [Game("dino-run", "./banner photos/dino-run.png", "./Dino_runGame/"), Game("doodle jump", "./banner photos/doodle-jump.png", "./Pygame-DoodleJump-main/")]

# Run until the user asks to quit
running = True
screen.fill((255, 255, 255))
game_index = -1
while running:
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game_index = (1 + game_index) % len(games)
                img = games[game_index].thumbnail
                rect = img.get_rect()
                rect.center = HIGH/2,WIDTH/2
                screen.blit(img, rect)
                pygame.draw.rect(screen, (255,0,0), rect, 1)

                
            elif event.key == pygame.K_LEFT:
                games[game_index].launch()
                running = False

    # Draw a solid blue circle in the center

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()