import numpy as np
import pygame
import sys
import time
import copy

# Initialize pygame
pygame.init()

# Constants for graphics
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CELL_SIZE = WIDTH // 8
KING_RED = (200, 0, 0)
KING_BLUE = (0, 0, 200)

class Checkers:
    def __init__(self):
        self.board = self.create_board()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.selected_piece = None
        self.current_player = 'R'  # Red always starts
        self.draw_board()
    
    def create_board(self):
        board = np.full((8, 8), '-')
        # Blue pieces
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'B'
        # Red pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'R'
        return board
    
    def draw_board(self):
        self.window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                # Alternate cell colors for a checkered pattern
                color = BLACK if (row + col) % 2 == 0 else WHITE
                pygame.draw.rect(self.window, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                piece = self.board[row][col]
                if piece in ['R', 'B']:
                    pygame.draw.circle(
                        self.window,
                        RED if piece == 'R' else BLUE,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 5
                    )
                elif piece in ['RK', 'BK']:
                    pygame.draw.circle(
                        self.window,
                        KING_RED if piece == 'RK' else KING_BLUE,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 5
                    )
        pygame.display.update()
    
    def valid_moves(self, row, col, board=None):
        """Return a list of valid move coordinates for the piece at (row, col)."""
        if board is None:
            board = self.board
        moves = []
        piece = board[row][col]
        if piece == '-':
            return moves
        # Check all four diagonal directions (for simplicity, both normal and king pieces can move in all directions)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Normal move
                if board[new_row][new_col] == '-':
                    moves.append((new_row, new_col))
                # Check if opponent piece is present for a jump (capture)
                elif board[new_row][new_col] != '-' and board[new_row][new_col][0] != piece[0]:
                    jump_row, jump_col = new_row + drow, new_col + dcol
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8 and board[jump_row][jump_col] == '-':
                        moves.append((jump_row, jump_col))
        return moves
    
    def move_piece(self, row, col):
        """Handles a move by a human player."""
        if self.selected_piece:
            old_row, old_col = self.selected_piece
            if (row, col) in self.valid_moves(old_row, old_col):
                self.board[row][col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = '-'
                # Capture move (jumping over an opponent)
                if abs(row - old_row) == 2:
                    mid_row, mid_col = (row + old_row) // 2, (col + old_col) // 2
                    self.board[mid_row][mid_col] = '-'
                # King promotion
                if row == 0 and self.board[row][col] == 'R':
                    self.board[row][col] = 'RK'
                elif row == 7 and self.board[row][col] == 'B':
                    self.board[row][col] = 'BK'
                # Check for win condition
                if not any('B' in cell for cell in self.board.flatten()):
                    print("Red wins!")
                    pygame.quit()
                    sys.exit()
                if not any('R' in cell for cell in self.board.flatten()):
                    print("Blue wins!")
                    pygame.quit()
                    sys.exit()
                self.current_player = 'B' if self.current_player == 'R' else 'R'
            self.selected_piece = None
        else:
            # Only allow moving your own piece
            if self.board[row][col] in [self.current_player, self.current_player + 'K']:
                self.selected_piece = (row, col)
    
    def simulate_move(self, board, start, end):
        """Return a new board state after simulating the move from start to end."""
        new_board = copy.deepcopy(board)
        sr, sc = start
        er, ec = end
        piece = new_board[sr][sc]
        new_board[er][ec] = piece
        new_board[sr][sc] = '-'
        # Capture move: remove the jumped-over opponent
        if abs(er - sr) == 2:
            mid_row, mid_col = (er + sr) // 2, (ec + sc) // 2
            new_board[mid_row][mid_col] = '-'
        # King promotion
        if er == 0 and piece == 'R':
            new_board[er][ec] = 'RK'
        if er == 7 and piece == 'B':
            new_board[er][ec] = 'BK'
        return new_board

    def get_all_moves(self, board, player):
        """Generate all possible moves for a given player and return tuples of (start, end, new_board)."""
        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] != '-' and board[r][c][0] == player:
                    valid = self.valid_moves(r, c, board)
                    for move in valid:
                        new_board = self.simulate_move(board, (r, c), move)
                        moves.append(((r, c), move, new_board))
        return moves

    def evaluate_board(self, board, ai_player):
        """
        Simple evaluation function:
         - Count pieces (normal pieces count as 1, kings as 1.5)
         - Return the score from the perspective of the AI player.
        """
        red_score = 0
        blue_score = 0
        for row in board:
            for piece in row:
                if piece == 'R':
                    red_score += 1
                elif piece == 'RK':
                    red_score += 1.5
                elif piece == 'B':
                    blue_score += 1
                elif piece == 'BK':
                    blue_score += 1.5
        if ai_player == 'R':
            return red_score - blue_score
        else:
            return blue_score - red_score

    def minimax(self, board, depth, maximizing, ai_player, node_counter):
        """Minimax algorithm (depth-limited) without pruning."""
        node_counter['count'] += 1
        if depth == 0:
            return self.evaluate_board(board, ai_player), board

        current_player = ai_player if maximizing else ('R' if ai_player == 'B' else 'B')
        moves = self.get_all_moves(board, current_player)
        if not moves:
            return self.evaluate_board(board, ai_player), board

        if maximizing:
            max_eval = float('-inf')
            best_move_board = None
            for move in moves:
                eval_value, _ = self.minimax(move[2], depth - 1, False, ai_player, node_counter)
                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move_board = move[2]
            return max_eval, best_move_board
        else:
            min_eval = float('inf')
            best_move_board = None
            for move in moves:
                eval_value, _ = self.minimax(move[2], depth - 1, True, ai_player, node_counter)
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move_board = move[2]
            return min_eval, best_move_board

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing, ai_player, node_counter):
        """Minimax algorithm with alpha-beta pruning."""
        node_counter['count'] += 1
        if depth == 0:
            return self.evaluate_board(board, ai_player), board

        current_player = ai_player if maximizing else ('R' if ai_player == 'B' else 'B')
        moves = self.get_all_moves(board, current_player)
        if not moves:
            return self.evaluate_board(board, ai_player), board

        if maximizing:
            max_eval = float('-inf')
            best_move_board = None
            for move in moves:
                eval_value, _ = self.minimax_alpha_beta(move[2], depth - 1, alpha, beta, False, ai_player, node_counter)
                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move_board = move[2]
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval, best_move_board
        else:
            min_eval = float('inf')
            best_move_board = None
            for move in moves:
                eval_value, _ = self.minimax_alpha_beta(move[2], depth - 1, alpha, beta, True, ai_player, node_counter)
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move_board = move[2]
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval, best_move_board

    def ai_move(self, use_alpha_beta, depth, ai_player):
        """Perform the AI move using the selected algorithm, and print performance metrics."""
        node_counter = {'count': 0}
        start_time = time.time()
        if use_alpha_beta:
            score, new_board = self.minimax_alpha_beta(self.board, depth, float('-inf'), float('inf'), True, ai_player, node_counter)
        else:
            score, new_board = self.minimax(self.board, depth, True, ai_player, node_counter)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"AI Move -> Depth: {depth}, Score: {score}, Nodes Expanded: {node_counter['count']}, Time: {exec_time:.4f} sec")
        self.board = new_board
        # Switch the current player after AI move
        self.current_player = 'R' if ai_player == 'B' else 'B'
        self.draw_board()

if __name__ == "__main__":
    # User configuration
    print("Welcome to Checkers!")
    mode = input("Select mode: 1 for Human vs AI, 2 for Human vs Human: ").strip()
    if mode not in ['1', '2']:
        print("Invalid mode. Exiting.")
        sys.exit()
    if mode == '1':
        # Let user choose their color (Red moves first)
        human_color = input("Do you want to play as Red (R) or Blue (B)? ").upper().strip()
        if human_color not in ['R', 'B']:
            print("Invalid choice. Defaulting to Red.")
            human_color = 'R'
        # AI will play the opposite color
        ai_player = 'B' if human_color == 'R' else 'R'
        algorithm_choice = input("Select AI algorithm: 1 for Minimax, 2 for Alpha-Beta Pruning: ").strip()
        use_alpha_beta = True if algorithm_choice == '2' else False
        try:
            depth = int(input("Enter AI depth limit (e.g., 3, 4, 5): ").strip())
        except ValueError:
            print("Invalid depth. Defaulting to 3.")
            depth = 3
    else:
        ai_player = None
        use_alpha_beta = False
        depth = 0

    game = Checkers()
    running = True
    while running:
        # If playing against the AI and it's the AI's turn, make the AI move
        if mode == '1' and game.current_player == ai_player:
            game.ai_move(use_alpha_beta, depth, ai_player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Human moves are allowed when it's not the AI’s turn or in Human vs Human mode
            if (mode == '1' and game.current_player != ai_player) or mode == '2':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    game.move_piece(row, col)
                    game.draw_board()
    pygame.quit()
