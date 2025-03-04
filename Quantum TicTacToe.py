import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
WHITE, BLACK, RED, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
FONT = pygame.font.Font(None, 60)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Tic-Tac-Toe")

# Game state
board = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
players = ['X', 'O']
turn = 0
collapsed_board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    """Draws the Tic-Tac-Toe grid."""
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 3)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 3)

def draw_board():
    """Displays the current game board."""
    screen.fill(WHITE)
    draw_grid()
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE + 20, row * CELL_SIZE + 20
            if collapsed_board[row][col]:
                text = FONT.render(collapsed_board[row][col], True, RED if collapsed_board[row][col] == 'X' else BLUE)
                screen.blit(text, (x + 30, y + 30))
            elif board[row][col]:
                text = FONT.render(", ".join(board[row][col]), True, BLACK)
                screen.blit(text, (x, y))

def check_winner():
    """Checks for a winner after collapse."""
    win_patterns = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    flat_board = [collapsed_board[row][col] for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
    
    for a, b, c in win_patterns:
        if flat_board[a] and flat_board[a] == flat_board[b] == flat_board[c]:
            return flat_board[a]
    return None

def collapse_board():
    """Collapses quantum states randomly when a cycle is detected."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if len(board[row][col]) > 1:
                collapsed_board[row][col] = random.choice(board[row][col])
            elif len(board[row][col]) == 1:
                collapsed_board[row][col] = board[row][col][0]

def main():
    global turn, board, collapsed_board
    running = True
    game_over = False
    
    while running:
        draw_board()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                
                if not collapsed_board[row][col]:
                    player = players[turn % 2]
                    board[row][col].append(player)
                    turn += 1
                    
                    # Check for collapse (when a cycle is detected)
                    if any(len(board[r][c]) > 1 for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
                        collapse_board()
                        winner = check_winner()
                        if winner:
                            print(f"Player {winner} wins!")
                            game_over = True

        if game_over:
            pygame.time.wait(2000)
            board = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            collapsed_board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            turn = 0
            game_over = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
