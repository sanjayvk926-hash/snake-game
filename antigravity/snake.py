import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("bahnschrift", 25)

def draw_snake(snake_body):
    """Draw the snake on the screen."""
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_apple(apple_pos):
    """Draw the apple on the screen."""
    pygame.draw.rect(screen, RED, [apple_pos[0], apple_pos[1], BLOCK_SIZE, BLOCK_SIZE])

def show_score(score):
    """Display the current score."""
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, [10, 10])

def game_over_screen():
    """Display the game over text."""
    screen.fill(BLACK)
    msg = font.render("Game Over! Press C to Play Again or Q to Quit", True, RED)
    
    # Center the message on the screen
    msg_rect = msg.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(msg, msg_rect)
    pygame.display.update()

def main():
    game_over = False
    game_close = False

    # Initial Snake position and movement
    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0
    
    snake_body = []
    snake_length = 1

    # Place the first apple at a random grid-aligned position
    apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:

        # Handling Game Over state
        while game_close:
            game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()  # Restart game loop
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                # Prevent snake from reversing direction immediately
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Check bounds (collision with walls)
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Update snake position based on movement
        x += x_change
        y += y_change

        # Clear the display
        screen.fill(BLACK)
        
        # Draw the apple
        draw_apple((apple_x, apple_y))

        # Update the snake's body coordinates
        snake_head = [x, y]
        snake_body.append(snake_head)
        
        # Maintain snake length by removing the tail if length hasn't increased
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check for collision with itself
        for block in snake_body[:-1]:
            if block == snake_head:
                game_close = True

        # Render the snake and score
        draw_snake(snake_body)
        show_score(snake_length - 1)  # Length starts at 1, so score is length - 1

        pygame.display.update()

        # Check if the snake ate an apple
        if x == apple_x and y == apple_y:
            # Generate a new random apple
            apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1  # Grow snake

        # Cap the frame rate
        clock.tick(FPS)

    # Cleanup before exiting
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
