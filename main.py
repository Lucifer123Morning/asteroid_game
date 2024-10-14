import sys
import pygame
import random  # Make sure to import random for stars
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def draw_stars(screen, num_stars):
    for _ in range(num_stars):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)  # Draw small white stars

def main():
    pygame.init()

    # Initialize the mixer
    pygame.mixer.init(frequency=22050, size=-16, channels=2)  # Optional: set the mixer parameters

    # Load background music and play it
    try:
        pygame.mixer.music.load('assets/background_music.wav')  # Ensure the path is correct
        pygame.mixer.music.set_volume(1)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play the music in a loop
    except pygame.error as e:
        print(f"Error loading music: {e}")
        print("Ensure the music file exists and is a supported format.")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Game state variables
    score = 0
    lives = 3  # Ensure the player starts with 3 lives
    mistakes = 0  # Counter for mistakes

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the music when quitting
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space to shoot
                    player.shoot()  # Ensure you implement the shoot method in the Player class

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                mistakes += 1  # Increment mistakes
                if mistakes >= 3:  # If mistakes reach 3, lose a life
                    lives -= 1
                    mistakes = 0  # Reset mistakes after losing a life
                    if lives <= 0:
                        print("Game over!")
                        pygame.mixer.music.stop()  # Stop the music when the game is over
                        sys.exit()  # Consider implementing a restart method instead

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 10  # Increment score for destroying an asteroid

        screen.fill("black")

        # Draw stars in the background
        draw_stars(screen, 100)  # Adjust the number of stars as needed

        for obj in drawable:
            obj.draw(screen)

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
