"""
    Author: Zak Groenewold, Dinesh Seveti, Arne Samuel
    Date: 11/20/2024
    CSCI310
    Pacman game utilizing multithreading
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

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.SysFont('Arial', 18) or pygame.font.Font(None, 18)

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

# Scaled Pac-Man and ghost images
pacman_sprite = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))

for i in range (len(ghost_images)):
    ghost_images[i] = pygame.transform.scale(ghost_images[i], (CELL_SIZE,CELL_SIZE))
    
def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y* CELL_SIZE + CELL_SIZE // 2), 3)
            elif cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 7)

# Draw Pac-Man and the ghosts
def draw_Pacman():
    screen.blit(pacman_sprite, (pacman_x * CELL_SIZE, pacman_y * CELL_SIZE))
    
def draw_ghosts():
    for i, ghost in enumerate(ghosts):
        screen.blit(ghost_images[i], (ghost['x'] * CELL_SIZE, ghost['y'] * CELL_SIZE))

# Function defines Pac-Man movement
def move_pacman():
    global pacman_x, pacman_y, score, pacman_direction 
    if pacman_direction == 'LEFT' and board[pacman_y][pacman_x - 1] != '#':
        pacman_x -= 1
    elif pacman_direction == 'RIGHT' and board[pacman_y][pacman_x + 1] != '#':
        pacman_x += 1
    elif pacman_direction == 'UP' and board[pacman_y - 1][pacman_x] != '#':
        pacman_y -= 1
    elif pacman_direction == 'DOWN' and board[pacman_y + 1][pacman_x] != '#':
        pacman_y += 1
    
    if board[pacman_y][pacman_x] == '.':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 10
    elif board[pacman_y][pacman_x] == 'o':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 50

# Function defines ghost movement
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
            
# Check for collisions with ghosts
def check_collisions():
    for ghost in ghosts:
        if ghost['x'] == pacman_x and ghost['y'] == pacman_y:
            return True
    return False

# Check if all pellets are eaten and game is won
def check_all_pellets_eaten():
    for row in board:
        if '.' in row or 'o' in row:
            return False
    return True

pacman_x, pacman_y = 1,1
pacman_direction = None
score = 0

# Initialize ghost and Pac-Man positions
# Global variables for positions
pacman_x, pacman_y = 1, 1  # Pac-Man starts at (1, 1)

ghosts = [
    {'x': 13, 'y': 11},  # Blinky
    {'x': 13, 'y': 12},  # Clyde
    {'x': 14, 'y': 11},  # Inky
    {'x': 14, 'y': 12}   # Pinky
]


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

    move_pacman()
    move_ghosts()

    if check_collisions():
        print("Game Over!")
        running = False

    if check_all_pellets_eaten():
        print("You Win!")
        running = False

    screen.fill(BLACK)
    draw_board()
    draw_Pacman()
    draw_ghosts()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()