import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Set custom screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800

# Set up the screen with custom dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hit the Mouse")

# Load images
current_dir = os.path.dirname(__file__)
background_image = pygame.image.load(os.path.join(current_dir, "background.jpg"))
mouse_image = pygame.image.load(os.path.join(current_dir, "mouse.png"))

# Set up fonts
font = pygame.font.SysFont(None, 36)

# Set up variables
score = 0
mouse_spawn_delay = 1000  # in milliseconds
last_mouse_spawn_time = 0
mice = []

# Define the Mouse class
class Mouse:
    def __init__(self):
        self.image = mouse_image
        self.rect = self.image.get_rect()

        # Check if the image dimensions are smaller than the screen dimensions
        if self.rect.width >= SCREEN_WIDTH or self.rect.height >= SCREEN_HEIGHT:
            raise ValueError("Mouse image size exceeds screen dimensions")

        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            self.speed = random.randint(1, 3)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Define the main game loop
def main():
    global score, last_mouse_spawn_time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for mouse in mice:
                    if mouse.rect.collidepoint(event.pos):
                        mice.remove(mouse)
                        score += 1

        current_time = pygame.time.get_ticks()
        if current_time - last_mouse_spawn_time > mouse_spawn_delay:
            mice.append(Mouse())
            last_mouse_spawn_time = current_time

        for mouse in mice:
            mouse.update()

        screen.blit(background_image, (0, 0))
        for mouse in mice:
            mouse.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
