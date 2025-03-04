"""
    Author: Dinesh Seveti
    Date: 11/24/2024
    CSCI 593
    Pacman game Collision Avoidance and synchronization
    Credit: 
        Some Code used from https://medium.com/dataflair/create-pacman-game-using-python-7dcedbbe74f1
"""






import pygame
import sys
import random

# Initialize pygame library
pygame.init()

# Settings for the game window
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
CELL_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize the screen and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.SysFont('Arial', 18) or pygame.font.Font(None, 18)

# Game board
board = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "       ## #      # ##       ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Load assets (Make sure these are available in the correct directory)
try:
    pacman_image = pygame.image.load('./assets/Pacman.png')
    ghost_images = [
        pygame.image.load('./assets/Blinky.png'),
        pygame.image.load('./assets/Clyde.png'),
        pygame.image.load('./assets/Inky.png'),
        pygame.image.load('./assets/Pinky.png')
    ]
except FileNotFoundError:
    print("Missing image assets, unable to render game.")
    sys.exit()

# Scale images to fit the cell size
pacman_sprite = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))
ghost_sprites = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in ghost_images]

# Shared resources (Position of Pac-Man and ghosts)
pacman_x, pacman_y = 1, 1
pacman_direction = None
score = 0

ghosts = [
    {'x': 13, 'y': 11},  # Blinky
    {'x': 13, 'y': 12},  # Clyde
    {'x': 14, 'y': 11},  # Inky
    {'x': 14, 'y': 12}   # Pinky
]

# Function to draw the game board
def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)
            elif cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 7)

# Function to move Pac-Man
def move_pacman():
    global pacman_x, pacman_y, pacman_direction, score
    if pacman_direction == 'LEFT' and board[pacman_y][pacman_x - 1] != '#':
        pacman_x -= 1
    elif pacman_direction == 'RIGHT' and board[pacman_y][pacman_x + 1] != '#':
        pacman_x += 1
    elif pacman_direction == 'UP' and board[pacman_y - 1][pacman_x] != '#':
        pacman_y -= 1
    elif pacman_direction == 'DOWN' and board[pacman_y + 1][pacman_x] != '#':
        pacman_y += 1

    # Eating pellets
    if board[pacman_y][pacman_x] == '.':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 10
    elif board[pacman_y][pacman_x] == 'o':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 50

# Function to move ghosts
def move_ghosts():
    for ghost in ghosts:
        direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        if direction == 'LEFT' and board[ghost['y']][ghost['x'] - 1] != '#':
            ghost['x'] -= 1
        elif direction == 'RIGHT' and board[ghost['y']][ghost['x'] + 1] != '#':
            ghost['x'] += 1
        elif direction == 'UP' and board[ghost['y'] - 1][ghost['x']] != '#':
            ghost['y'] -= 1
        elif direction == 'DOWN' and board[ghost['y'] + 1][ghost['x']] != '#':
            ghost['y'] += 1

# Function to check for collisions with ghosts
def check_collisions():
    for ghost in ghosts:
        if ghost['x'] == pacman_x and ghost['y'] == pacman_y:
            return True
    return False

# Function to check if all pellets are eaten and the game is won
def check_all_pellets_eaten():
    for row in board:
        if '.' in row or 'o' in row:
            return False
    return True

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                pacman_direction = 'RIGHT'
            elif event.key == pygame.K_UP:
                pacman_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                pacman_direction = 'DOWN'

    # Move Pac-Man and ghosts
    move_pacman()
    move_ghosts()

    # Check if Pac-Man collided with any ghost
    if check_collisions():
        print("Game Over!")
        running = False

    # Check if all pellets are eaten
    if check_all_pellets_eaten():
        print("You Win!")
        running = False

    # Draw everything on the screen
    screen.fill(BLACK)
    draw_board()

    # Draw Pac-Man
    screen.blit(pacman_sprite, (pacman_x * CELL_SIZE, pacman_y * CELL_SIZE))

    # Draw ghosts
    for i, ghost in enumerate(ghosts):
        screen.blit(ghost_sprites[i], (ghost['x'] * CELL_SIZE, ghost['y'] * CELL_SIZE))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
