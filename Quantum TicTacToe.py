import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
WHITE, BLACK, RED, BLUE, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0)
FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 30)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Tic-Tac-Toe")

# Game state
board = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
quantum_moves = {}  # Tracks quantum moves before collapse
players = ['X', 'O']
turn = 0
collapsed_board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
highlighted_cell = None

def draw_grid():
    """Draws the Tic-Tac-Toe grid."""
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 3)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 3)

def draw_board():
    """Displays the current game board."""
    screen.fill(WHITE)
    draw_grid()

    if highlighted_cell:
        pygame.draw.rect(screen, GREEN, (highlighted_cell[1] * CELL_SIZE, highlighted_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE + 20, row * CELL_SIZE + 20
            if collapsed_board[row][col]:
                text = FONT.render(collapsed_board[row][col], True, RED if collapsed_board[row][col] == 'X' else BLUE)
                screen.blit(text, (x + 30, y + 30))
            elif (row, col) in quantum_moves:
                for i, symbol in enumerate(quantum_moves[(row, col)]):
                    color = RED if symbol == 'X' else BLUE
                    text = SMALL_FONT.render(symbol, True, color)
                    screen.blit(text, (x, y + (i * 20)))

def collapse_board():
    """Collapses the board by resolving quantum moves."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row, col) in quantum_moves:
                collapsed_board[row][col] = random.choice(quantum_moves[(row, col)])

def check_winner():
    """Checks for a winner after collapse."""
    for row in range(GRID_SIZE):
        if collapsed_board[row][0] and collapsed_board[row][0] == collapsed_board[row][1] == collapsed_board[row][2]:
            return collapsed_board[row][0]
    for col in range(GRID_SIZE):
        if collapsed_board[0][col] and collapsed_board[0][col] == collapsed_board[1][col] == collapsed_board[2][col]:
            return collapsed_board[0][col]
    if collapsed_board[0][0] and collapsed_board[0][0] == collapsed_board[1][1] == collapsed_board[2][2]:
        return collapsed_board[0][0]
    if collapsed_board[0][2] and collapsed_board[0][2] == collapsed_board[1][1] == collapsed_board[2][0]:
        return collapsed_board[0][2]
    return None

def display_message(message):
    """Displays a temporary message on the screen."""
    screen.fill(WHITE)
    text = FONT.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    """Resets the game state after a win."""
    global board, collapsed_board, turn, quantum_moves, highlighted_cell
    board = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    collapsed_board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    quantum_moves = {}
    turn = 0
    highlighted_cell = None

def main():
    global turn, quantum_moves, collapsed_board, highlighted_cell
    running = True
    game_over = False

    while running:
        draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                highlighted_cell = (y // CELL_SIZE, x // CELL_SIZE)

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE

                player = players[turn % 2]
                if (row, col) not in quantum_moves:
                    quantum_moves[(row, col)] = []
                quantum_moves[(row, col)].append(player)
                draw_board()
                pygame.display.flip()
                turn += 1
                collapse_board()

                winner = check_winner()
                if winner:
                    display_message(f"Player {winner} wins!")
                    game_over = True

        if game_over:
            reset_game()
            game_over = False

    pygame.quit()

if __name__ == "__main__":
    main()
