import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Font for displaying the score
font = pygame.font.SysFont('arial', 24)

# Clock to control the speed
clock = pygame.time.Clock()

# Snake initialization
snake = [(100, 100), (80, 100), (60, 100)] # List of (x, y) segments
snake_direction = 'RIGHT'
change_to = snake_direction

# Food initialization
food_position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) -1) * CELL_SIZE,
                 random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) -1) * CELL_SIZE)
food_spawned = True

# Game variables
score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction == 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and not snake_direction == 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and not snake_direction == 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and not snake_direction == 'LEFT':
                change_to = 'RIGHT'

    # Update the direction
    snake_direction = change_to

    # Move the snake
    if snake_direction == 'UP':
        new_head = (snake[0][0], snake[0][1] - CELL_SIZE)
    elif snake_direction == 'DOWN':
        new_head = (snake[0][0], snake[0][1] + CELL_SIZE)
    elif snake_direction == 'LEFT':
        new_head = (snake[0][0] - CELL_SIZE, snake[0][1])
    elif snake_direction == 'RIGHT':
        new_head = (snake[0][0] + CELL_SIZE, snake[0][1])

    snake.insert(0, new_head)

    # Check if the snake has eaten the food
    if snake[0] == food_position:
        score += 10
        food_spawned = False
    else:
        snake.pop()

    # Spawn new food
    if not food_spawned:
        food_position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        food_spawned = True

    # Check for collisions with boundaries or itself
    if (snake[0][0] < 0 or snake[0][0] >= SCREEN_WIDTH or
            snake[0][1] < 0 or snake[0][1] >= SCREEN_HEIGHT or
            snake[0] in snake[1:]):
        running = False
    # Draw everything
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

    # Render and display the score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the speed
    clock.tick(10)

pygame.quit()