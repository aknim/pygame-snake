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
BLUE = (0, 0, 255)

#Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Font for displaying the score & game over message
font = pygame.font.SysFont('arial', 24)
game_over_font = pygame.font.SysFont('arial', 48)

# Clock to control the speed
clock = pygame.time.Clock()
high_score = 0
borderLess_mode = True

# Load sound effects
eat_sound = pygame.mixer.Sound('eat1.mp3')
crash_sound = pygame.mixer.Sound('crash.wav')


# Reset Game
def reset_game():
    global snake, snake_direction, change_to, food_position, food_spawned, score, running
    global speed, level, obstacles

    snake = [(100, 100), (80, 100), (60, 100)] # List of (x, y) segments
    snake_direction = 'RIGHT'
    change_to = snake_direction

    food_position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) -1) * CELL_SIZE,
                     random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) -1) * CELL_SIZE)
    food_spawned = True

    score = 0
    speed = 10
    level = 1
    obstacles = []
    running = True

def generate_obstacles():
    obstacles = []
    for _ in range(level):
        obstacle_x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE)) * CELL_SIZE
        obstacle_y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE)) * CELL_SIZE
        obstacles.append((obstacle_x, obstacle_y))
    return obstacles


# Function to display the game over message
def show_game_over():
    game_over_text = game_over_font.render('GAME OVER', True, RED)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    restart_text = font.render('Press R to Restart', True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    screen.blit(high_score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 30))
    screen.blit(restart_text, (SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()
    #pygame.time.wait(3000) # Wait for 3 seconds before closing

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_restart = False
                global running
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_restart = False
                    reset_game()

reset_game()

# Main game loop
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

    if borderLess_mode:
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

    snake.insert(0, new_head)

    # Check if the snake has eaten the food
    if snake[0] == food_position:
        score += 10
        eat_sound.play()
        if score > high_score:
            high_score = score
        food_spawned = False
        # Increase speed
        if score % 50 == 0:
            speed += 1 
            level += 1
            obstacles = generate_obstacles()
    else:
        snake.pop()

    # Spawn new food
    while not food_spawned or food_spawned in obstacles:
        food_position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        food_spawned = True

    # Check for collisions with boundaries or itself
    if (snake[0][0] < 0 or snake[0][0] >= SCREEN_WIDTH or
            snake[0][1] < 0 or snake[0][1] >= SCREEN_HEIGHT or
            snake[0] in snake[1:] or
            any(obstacle == snake[0] for obstacle in obstacles)):
        crash_sound.play()
        show_game_over()

    # Draw everything
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, pygame.Rect(obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE))

    # Render and display the score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (10, 40))
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    hs_text_width, _ = font.size(f'High Score: {high_score}')
    screen.blit(high_score_text, (SCREEN_WIDTH - hs_text_width - 10, 10))

    # Update the display
    pygame.display.flip()

    # Control the speed
    clock.tick(speed)

pygame.quit()